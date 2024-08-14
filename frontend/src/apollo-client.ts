
import { ApolloClient, InMemoryCache, createHttpLink } from '@apollo/client/core';
import { provideApolloClient } from '@vue/apollo-composable';
import { createApp } from 'vue';

console.log('IMACOMPUTER'); // This logs when the setup function is called


const httpLink = createHttpLink({
  uri: 'http://localhost:8000/graphql/', // Your Django GraphQL endpoint
});

const cache = new InMemoryCache();

const apolloClient = new ApolloClient({
  link: httpLink,
  cache,
});

export function setupApollo(app: ReturnType<typeof createApp>) {
  console.log('Setting up Apollo Client with Vue...'); // This logs when the setup function is called
  provideApolloClient(apolloClient);
  app.provide('apollo', apolloClient);
}