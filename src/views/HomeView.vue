<template>
  <div class="home">
    <p @click="test">Click</p>
    <img alt="Vue logo" src="../assets/logo.png">
    <HelloWorld msg="Welcome to Your Vue.js App"/>

  </div>
</template>

<script>
// @ is an alias to /src
import HelloWorld from '@/components/HelloWorld.vue'

export default {
  name: 'HomeView',
  components: {
    HelloWorld
  },
  methods: {
    async test() {
      fetch("http://localhost:5000/login?include_auth_token", {
        method: "POST",
        body : JSON.stringify({
          "email":"a@gmail.com",
          "password":"qwerty"
        }),
        headers: {
            "Content-type": "application/json; charset-UTF-8"
          }
      })
      .then(response => response.json())
      .then(data => console.log(data))
    }
  }
}
</script>
