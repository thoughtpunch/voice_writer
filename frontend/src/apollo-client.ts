// src/apollo-client.ts
import { ApolloClient, InMemoryCache, createHttpLink } from '@apollo/client/core';
import { DefaultApolloClient } from '@vue/apollo-composable';
import { provideApolloClient } from '@vue/apollo-composable';
import { createApp } from 'vue';

const httpLink = createHttpLink({
  uri: 'http://localhost:8000/graphql/', // Your Django GraphQL endpoint
});

const cache = new InMemoryCache();

const apolloClient = new ApolloClient({
  link: httpLink,
  cache,
});

export function setupApollo(app: ReturnType<typeof createApp>) {
    provideApolloClient(apolloClient);
    app.provide(DefaultApolloClient, apolloClient);
  }