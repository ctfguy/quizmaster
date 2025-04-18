<script setup>
import { ref } from 'vue';
import NavBar from './NavBar.vue';
import axiosClient from '@/axiosClient';
import router from '@/router';
import { useUserStore } from '@/stores/user';

const email = ref("")
const password = ref("")
const loading = ref(false)

const store = useUserStore()

async function submit(event) {
    loading.value=true
    axiosClient.post('/auth/login', {email: email.value, password: password.value})
    .then((response) => {
        // Store the JWT token in localStorage
        if (response.data.access_token) {
            localStorage.setItem('token', response.data.access_token);
        }
        
        const user = response.data.user
        store.$patch({
            id: user.id,
            email: user.email,
            name: user.full_name,
            role: user.role
        })
        router.push({ path: `/${user.role}/dashboard`, replace: true })
    }).catch((error) => {
        alert(error.response.data.error)
    }).finally(() => {
        loading.value = false
    })
}
</script>

<template>
    <NavBar />
    <v-main>
        <v-container class="d-flex flex-column ga-6 justify-center h-100" max-width="600">
            <div class="text-h5 text-center">Welcome back! Enter your details!</div>
            <v-sheet rounded class="pa-4">

                <v-form @submit.prevent="submit">
                    <v-text-field label="Email" type="email" :disabled="loading" v-model="email" variant="solo-filled" required></v-text-field>
                    <v-text-field label="Password" type="password" :disabled="loading" v-model="password" variant="solo-filled" required></v-text-field>
                    <div class="d-flex justify-center">
                        <v-btn :loading="loading" color="success" type="submit" variant="elevated">Submit</v-btn>
                    </div>
                </v-form>
            </v-sheet>
        </v-container>
    </v-main>
</template>