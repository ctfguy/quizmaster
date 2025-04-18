<template>
    <v-app-bar>
        <v-app-bar-title>
            QuizMaster
        </v-app-bar-title>
        <template v-if="auth" v-slot:append>
            <v-btn variant="text" color="error" @click="logout">Logout</v-btn>
        </template>
    </v-app-bar>
</template>

<script setup>
    import axiosClient from '@/axiosClient';
    import router from '@/router';
    import { useUserStore } from '@/stores/user';
    import { ref } from 'vue';

    const store = useUserStore()

    const auth = ref(store.role != "")

    const logout = () => {
        axiosClient.post("/auth/logout").then(() => {
            // Remove the token from localStorage
            localStorage.removeItem('token');
            
            // Reset store state
            store.$patch({
                id: -1,
                email: "",
                name: "",
                role: ""
            })
            router.push("/")
        })
    }
</script>

<style>
    .custom-nav {
        text-decoration: none;
        color: rgb(250, 250, 250);
    }
</style>