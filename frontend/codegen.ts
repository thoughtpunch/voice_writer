
import type { CodegenConfig } from '@graphql-codegen/cli';

const config: CodegenConfig = {
  overwrite: true,
  schema: "http://localhost:8000/graphql/",
  documents: ["src/graphql/**/*.graphql", "src/**/*.vue"],
  generates: {
    "src/generated/": {
      preset: "client",
      plugins: [
        "typescript",
        "typescript-operations",
        "typescript-vue-apollo"
      ]
    },
    "./graphql.schema.json": {
      plugins: ["introspection"]
    }
  }
};

export default config;
