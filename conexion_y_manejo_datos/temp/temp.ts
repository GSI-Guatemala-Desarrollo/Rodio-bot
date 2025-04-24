import { FLOW_COLL, FLOW_TAGS_COLL, FLOW_TEMPLATE_COLL, database } from "$/db";
import { uploadFile } from "$/impl/blob";
import {
  calcAllExpressions,
  evalExpr,
  objectContext,
  readonlyObjectContext,
  type ContextManager,
} from "$/impl/expression";
import { getExternalFns } from "$/impl/externalFns";
import type {
  ValidationErrorObj,
  ValidatorReturnType,
} from "$/impl/validation";
import { verifyAuthenticated } from "$/jwt";
import { SExpression } from "$/models/expression";
import type { FinishedStage, Flow, FlowTag } from "$/models/flow";
import type { FlowTemplate } from "$/models/flowtemplate";
import {
  SCalculatedFormStage,
  validateFormStage,
  type FormStage,
} from "$/models/form";
import { kvdb } from "$/redis";
import {
  arrayFromAwait,
  arrayMapAsync,
  stringToId,
  tryObjectId,
} from "$/utils";
import type { MultipartFile, MultipartValue } from "@fastify/multipart";
import type { TypeBoxTypeProvider } from "@fastify/type-provider-typebox";
import { Type } from "@sinclair/typebox";
import { TypeCompiler } from "@sinclair/typebox/compiler";
import { compare } from "fast-json-patch/index.mjs";
import type { FastifyInstance } from "fastify";
import jwt from "jsonwebtoken";
import { ObjectId, type Db, type WithId } from "mongodb";

const vCalculatedFormStage = TypeCompiler.Compile(SCalculatedFormStage, [
  SExpression,
]);

async function calculateForm(
  id_empresa: string,
  stage: FormStage,
  contexts: ContextManager,
  keepValidationErrors: boolean,
  inLive: boolean,
  externalMemo: Record<string, any>
) {
  const formData = await calcAllExpressions(
    {
      externalMemo,
      contexts,
      external: {
        ...(await getExternalFns(database, id_empresa, "form")),
        inLive: {
          description: "InLive",
          lazy: false,
          nonMemoizable: true,
          fn: () => inLive,
        },
      },
      skip: [
        "postprocess",
        "nextStageId",
        "sections.#.postprocess",
        "sections.#.fields.#.liveValue",
        "sections.#.fields.#.postprocess",
        "sections.#.fields.#.livePostprocess",
      ],
      merge: ["sections.#", "sections.#.fields.#"],
    },
    stage
  );

  if (!vCalculatedFormStage.Check(formData)) {
    if (keepValidationErrors) {
      return validateFormStage.validator(formData) as {
        has_errors: true;
        errors: ValidationErrorObj["errors"];
        value: ValidatorReturnType<typeof validateFormStage>;
      };
    } else {
      return {
        has_errors: true as const,
        errors: [] as const,
        value: null,
      };
    }
  }

  return {
    has_errors: false as const,
    errors: [] as const,
    value: formData,
  };
}

export async function flowAssigned(
  database: Db,
  id_empresa: string,
  userId: string
) {
  const flowColl = database.collection(FLOW_COLL);
  return await arrayFromAwait(
    flowColl.find<Flow>(
      {
        id_empresa: id_empresa,
        $or: [{ assigned: null }, { assigned: userId }],
        currentStageId: { $ne: null },
      },
      {
        projection: {
          finishedStages: 0,
          globalData: 0,
          "template.stages": 0,
          "template.visualStageSequence": 0,
          "template.globalDataSpecs": 0,
          "template.visualGlobalDataSequence": 0,
        },
      }
    )
  );
}


export default async function routes(
  rawFastify: FastifyInstance,
  _options: object
) {
  const fastify = rawFastify.withTypeProvider<TypeBoxTypeProvider>();



  fastify.get(
    "/assigned/:id_empresa",
    {
      schema: {
        params: Type.Object({
          id_empresa: Type.String(),
        }),
      },
      onRequest: fastify.auth([verifyAuthenticated()]) as any,
    },
    async (req, reply) => {
      reply.send({
        code: 0,
        data: await flowAssigned(
          database,
          req.params.id_empresa,
          req.basic_user!.id
        ),
      });
    }
  );



  export async function flowCurrent(
    database: Db,
    id_empresa: string,
    id_user: string,
    flowId: ObjectId | string,
    keepValidationErrors: boolean = false
  ) {
    const flowColl = database.collection(FLOW_COLL);
    const flowData = await flowColl.findOne<WithId<Flow>>({
      [flowId instanceof ObjectId ? "_id" : "firebase_id"]: flowId,
      id_empresa: id_empresa,
    });
    if (flowData === null) return null;
    const externalMemo: Record<string, any> = {};
    if (flowData.currentStageId === null)
      return {
        flowData,
        public: {
          _id: null,
          name: null,
          type: null,
          finishedStages: flowData.finishedStages,
          data: null,
          templateInfo: {
            name: flowData.template.name,
            lastTemplateVersion: flowData.template.updateDate,
            lastTemplateUpdate: flowData.lastTemplateUpdateDate,
          },
        },
        raw: {
          name: null,
          type: null,
          data: null,
        },
        externalMemo,
      };
  
    const currentStage = flowData.template.stages[flowData.currentStageId];
    if (currentStage === undefined)
      return {
        flowData,
        public: {
          _id: null,
          name: null,
          type: null,
          finishedStages: flowData.finishedStages,
          data: null,
        },
        raw: {
          name: null,
          type: null,
          data: null,
        },
        externalMemo,
      };
  
    if (currentStage.type === "form") {
      if (flowData.assigned !== null && !flowData.assigned.includes(id_user))
        return {
          flowData,
          public: {
            _id: flowData.currentStageId,
            name: currentStage.name,
            type: currentStage.type,
            finishedStages: flowData.finishedStages,
            data: null,
            assigned: false,
          },
          raw: {
            ...currentStage,
            data: null,
          },
          externalMemo,
        };
  
      const validatedFormData = await calculateForm(
        id_empresa,
        currentStage.data,
        objectContext(
          { local: {} },
          readonlyObjectContext({
            global: flowData.globalData,
            arg: {
              // IDs
              id_empresa,
              id_user,
              flowId: flowData._id,
              templateId: flowData.templateId.toString(),
            },
          })
        ),
        keepValidationErrors,
        false,
        externalMemo
      );
  
      const returnBody = {
        flowData,
        public: {
          _id: flowData.currentStageId,
          name: currentStage.name,
          type: currentStage.type,
          finishedStages: flowData.finishedStages,
          data:
            validatedFormData.value !== null &&
            !("VALIDATION_ERROR" in validatedFormData.value)
              ? {
                  sections: validatedFormData.value.sections,
                }
              : null,
          assigned: true,
          token: "",
        },
        raw: {
          ...currentStage,
          data: validatedFormData,
        },
        externalMemo,
      };
  
      const token = jwt.sign(
        { id_user: id_user, flowId: flowId },
        `66947736116694773611`,
        {
          expiresIn: "1h",
        }
      );
      kvdb.set(`flow_form_${token}`, JSON.stringify(returnBody), {
        EX: 1 * 60 * 60,
      });
      returnBody.public.token = `flow_form_${token}`;
      return returnBody;
    } else {
      return {
        flowData,
        public: {
          _id: flowData.currentStageId,
          name: currentStage.name,
          type: currentStage.type,
          finishedStages: flowData.finishedStages,
          data: null,
          assigned: null,
        },
        raw: currentStage,
        externalMemo,
      };
    }
  }
  

  fastify.get(
    "/current/:id_empresa/:flowId",
    {
      schema: {
        params: Type.Object({
          id_empresa: Type.String(),
          flowId: Type.String(),
        }),
      },
      onRequest: fastify.auth([verifyAuthenticated()]) as any,
    },
    async (req, reply) => {
      reply.send({
        code: 0,
        data:
          (
            await flowCurrent(
              database,
              req.params.id_empresa,
              req.basic_user!.id,
              tryObjectId(req.params.flowId) ?? req.params.flowId,
              true
            )
          )?.public ?? null,
      });
    }
  );
}
