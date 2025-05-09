import type { JSONSchema7 } from 'json-schema';
import type { VuetifyOptions } from 'vuetify';
import Ajv from 'ajv/dist/2020';

import { cloneDeep, pickBy } from 'lodash';
import type {
  DandiModel,
  BasicSchema,
  BasicArraySchema,
  ComplexSchema,
} from './types';
import {
  isArraySchema,
  isBasicEditorSchema,
  isComplexEditorSchema,
} from './types';
import type { EditorInterface } from './editor';

export function computeBasicSchema(schema: JSONSchema7): JSONSchema7 {
  const newProperties = pickBy(schema.properties, (val): val is BasicSchema | BasicArraySchema => (
    isBasicEditorSchema(val)
  ));
  const newRequired = schema.required?.filter(
    (key) => Object.keys(newProperties).includes(key),
  ) || [];
  const newSchema = {
    ...schema,
    properties: newProperties,
    required: newRequired,
  };

  // Title and description aren't needed and just causes rendering issues
  delete newSchema.title;
  delete newSchema.description;
  // $schema isn't needed and causes Ajv to throw an error
  delete newSchema.$schema;
  return newSchema;
}

export function computeComplexSchema(schema: JSONSchema7): JSONSchema7 {
  const newProperties = pickBy(schema.properties, (val): val is ComplexSchema => (
    isComplexEditorSchema(val)
  ));
  const newRequired = schema.required?.filter(
    (key) => Object.keys(newProperties).includes(key),
  ) || [];
  const newSchema = {
    ...schema,
    properties: newProperties,
    required: newRequired,
  };

  // Description isn't needed and just causes rendering issues
  delete newSchema.description;
  return newSchema;
}

export function populateEmptyArrays(schema: JSONSchema7, model: DandiModel) {
  // TODO: May need to create a similar function for objects

  if (schema.properties === undefined) { return; }

  const props = schema.properties;
  const arrayFields = Object.keys(props).filter(
    (key) => isArraySchema(props[key]),
  );

  arrayFields.forEach((key) => {
    if (model[key] === undefined || model[key] === null) {
      model[key] = [];
    }
  });
}

export function filterModelWithSchema(model: DandiModel, schema: JSONSchema7): DandiModel {
  const { properties } = schema;
  if (!properties) { return {}; }

  return Object.keys(model).filter(
    (key) => properties[key] !== undefined,
  ).reduce(
    (obj, key) => ({ ...obj, [key]: cloneDeep(model[key]) }),
    {},
  );
}

export function writeSubModelToMaster(
  subModel: DandiModel, subSchema: JSONSchema7, masterModel: DandiModel,
) {
  const propsToWrite = subSchema.properties;
  if (propsToWrite === undefined) { return; }

  Object.keys(propsToWrite).forEach((key) => {
    masterModel[key] = subModel[key];
  });

}

export const VJSFVuetifyDefaultProps: VuetifyOptions['defaults'] = {
  global: {
    variant: 'outlined',
    density: 'compact',
  },
};

/**
 * Validates the metadata models of the editor interface using Ajv.
 * It checks the basic model and complex model against their respective schemas.
 * If the models are not valid, it sets the corresponding validation flags to false
 * to trigger the error state in the UI.
 *
 * This is needed because we do not currently feed the entire complex model and schema
 * into VJSF for validation. Instead, we only pass a single sub-model and schema into
 * VJSF when it has been selected by the "Edit" button. This means that validation errors
 * that apply to the entire complex model will not be caught until the user clicks "Save"
 * and the entire model is validated on the server. This function is a workaround to
 * validate the entire complex model on the client side.
 */
export const validateDandisetMetadata = (editorInterface: EditorInterface) => {
  const ajv = new Ajv({ allErrors: true, strict: false, verbose: true });

  // Update the basic model validation flag.
  editorInterface.basicModelValid.value = ajv.compile(editorInterface.basicSchema)(editorInterface.basicModel.value);

  // Update the complex model validation flags. Because the complex model is an object mapping
  // subschema names to their validation status, we need set each subschema's validation status
  // individually.
  const validateComplexModel = ajv.compile(editorInterface.complexSchema);
  validateComplexModel(editorInterface.complexModel);

  const invalidFields = new Set(validateComplexModel.errors?.map((error) => error.instancePath.split('/')[1]));
  for (const key in editorInterface.complexModelValidation) {
    editorInterface.complexModelValidation[key] = !invalidFields.has(key);
  }
};
