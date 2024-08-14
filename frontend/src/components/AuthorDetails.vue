<template>
    <div v-if="author">
        <h1>{{ author.firstName }} {{ author.lastName }}</h1>
        <p>{{ author.penName }}</p>
    </div>
</template>

<script lang="ts">
    import { defineComponent } from 'vue';
    import { useAuthorQuery } from '@/generated/graphql'; // Import the generated hook

    export default defineComponent({
    setup() {
        const { result: author, loading, error } = useAuthorQuery({
        variables: { id: '1' }, // Example ID
        });

        return {
        author,
        loading,
        error,
        };
    },
    });
</script>