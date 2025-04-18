<script setup>
import { ref } from 'vue';
import NavBar from './NavBar.vue';
import axiosClient from '@/axiosClient';
import router from '@/router';

const email = ref("")
const name = ref("")
const password = ref("")
const qualification = ref("")
const repassword = ref("")
const dob = ref("")
const number = ref("")
const loading = ref(false)

async function submit(event) {
    loading.value=true
    const reqBody = {
        email: email.value,
        password: password.value,
        full_name: name.value,
        phone_number: number.value,
        qualification: qualification.value,
        dob: new Date(dob.value).toISOString()
    }
    axiosClient.post("/auth/register", reqBody).then((data) => {
        alert("User created succesfully")
        router.push("/login")
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
                    <v-text-field label="Name" type="text" :disabled="loading" v-model="name" variant="solo-filled" required></v-text-field>
                    <v-text-field label="Email" type="email" :disabled="loading" v-model="email" variant="solo-filled" required></v-text-field>
                    <v-text-field label="Phone Number" type="string" :disabled="loading" v-model="number" variant="solo-filled" required></v-text-field>
                    <v-text-field label="Qualification" type="text" :disabled="loading" v-model="qualification" variant="solo-filled" required></v-text-field>
                    <v-text-field label="Date of Birth" type="date" :disabled="loading" v-model="dob" variant="solo-filled" required></v-text-field>
                    <v-text-field label="Password" type="password" :disabled="loading" v-model="password" variant="solo-filled" required></v-text-field>
                    <v-text-field label="Re-enter Password" type="password" :disabled="loading" v-model="repassword" variant="solo-filled" required></v-text-field>
                    <div class="d-flex justify-center">
                        <v-btn :loading="loading" color="success" type="submit" variant="elevated">Submit</v-btn>
                    </div>
                </v-form>
            </v-sheet>
        </v-container>
    </v-main>
</template>