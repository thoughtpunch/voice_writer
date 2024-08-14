import { createApp } from 'vue'
import App from './App.vue'
import { setupApollo } from './apollo-client';

createApp(App).mount('#app')


// src/main.ts
import { createApp } from 'vue';
import App from './App.vue';
import { setupApollo } from './apollo-client';

const app = createApp(App);

setupApollo(app);

app.mount('#app');