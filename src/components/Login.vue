<template>
<div class="login-page">
   <transition name="fade">
      <div v-if="!registerActive" class="wallpaper-login"></div>
   </transition>
   <div class="wallpaper-register"></div>

   <div class="container">
      <div class="row">
         <div class="col-lg-4 col-md-6 col-sm-8 mx-auto">
            <div v-if="!registerActive" class="card login" v-bind:class="{ error: emptyFields }">
               <h1>Sign In</h1> <br>
               <form class="form-group" @submit.prevent>
                  <input v-model="emailLogin" type="email" class="form-control" placeholder="Email" required> <br>
                  <input v-model="passwordLogin" type="password" class="form-control" placeholder="Password" required> <br>
                  <input type="submit" class="btn btn-primary" @click="doLogin"> <br> <br>
                  <p>Don't have an account? <a href="#" @click="registerActive = !registerActive, emptyFields = false">Sign up here</a> <br>
                  </p>
               </form>
            </div>

            <div v-else class="card register" v-bind:class="{ error: emptyFields }">
               <h1>Sign Up</h1> <br>
               <form class="form-group" @submit.prevent>
                  <input v-model="nameReg" type="text" class="form-control" placeholder="Name" required> <br>
                  <input v-model="emailReg" type="email" class="form-control" placeholder="Email" required> <br>
                  <input v-model="passwordReg" type="password" class="form-control" placeholder="Password" required> <br>
                  <input type="submit" class="btn btn-primary" @click="doRegister"> <br><br>
                  <p>Already have an account? <a href="#" @click="registerActive = !registerActive, emptyFields = false">Sign in here</a>
                  </p>
               </form>
            </div>
         </div>
      </div>

   </div>
</div>
</template>

<script>


export default {
    name: "Login_kanban",
   data: function() {
    return {
      registerActive: false,
      emailLogin: "",
      passwordLogin: "",
      emailReg: "",
      passwordReg: "",
      nameReg: "",
      emptyFields: false,
      access_token:""
    }
   },

   methods: {
      async doLogin() {
         if (this.emailLogin === "" || this.passwordLogin === "") {
            this.emptyFields = true;
         } else {
            const loginRequest = await fetch(`http://localhost:5000/login?include_auth_token`, {
            method: "POST",
            body: JSON.stringify({
               email: this.emailLogin,
               password: this.passwordLogin
            }),
            headers: {
               "Content-type": "application/json; charset-UTF-8",
            }
            })
            const jResponse = await loginRequest.json()
            this.access_token = jResponse.response.user.authentication_token
            this.current_user_id = jResponse.response.user.id
            localStorage.clear()
            localStorage.setItem("access_token", this.access_token)
            localStorage.setItem("current_user_id", this.current_user_id)
            console.log(this.access_token)
            console.log(this.current_user_id)
            if (localStorage.getItem('access_token')) {
               this.$router.push({name:'dashboard'})
            }
         }
      },
      
      async doRegister() {
         if (this.emailReg === "" || this.passwordReg === "" || this.nameReg === "") {
            this.emptyFields = true;
         } 
         else {
            const regRequest = await fetch(`http://localhost:5000/signup`, {
            method: "POST",
            body: JSON.stringify({
               name:this.nameReg,
               email: this.emailReg,
               password: this.passwordReg
            }),
            headers: {
               "Content-type": "application/json; charset-UTF-8"
            }
            })
            const message = await regRequest.json()
            console.log(message)
            if (message.msg=='Registration successful') {
               this.registerActive = !this.registerActive
            }
         }
      }
   },
   beforeCreate: function() {
      if (localStorage.getItem('access_token')) {
         this.$router.push({name:'dashboard'})
      }
   }
};

</script>

<style scoped>
p {
   line-height: 1rem;
}

.card {
   padding: 20px;
}

.form-group {
   margin-bottom: 20px;
}

.login-page {
   align-items: center;
   display: flex;
   height: 50vh;
}
.wallpaper-login {
      background: url(https://images.pexels.com/photos/32237/pexels-photo.jpg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260)
         no-repeat center center;
      background-size: cover;
      height: 100%;
      position: absolute;
      width: 100%;
   }

   .wallpaper-register {
      background: url(https://images.pexels.com/photos/533671/pexels-photo-533671.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260)
         no-repeat center center;
      background-size: cover;
      height: 100%;
      position: absolute;
      width: 100%;
      z-index: -1;
   }

   h1 {
      margin-bottom: 1.5rem;
   }

.error {
   animation-name: errorShake;
   animation-duration: 0.3s;
}

@keyframes errorShake {
   0% {
      transform: translateX(-25px);
   }
   25% {
      transform: translateX(25px);
   }
   50% {
      transform: translateX(-25px);
   }
   75% {
      transform: translateX(25px);
   }
   100% {
      transform: translateX(0);
   }
}
.login-page[data-v-ef68022e] {
    align-items: center;
    display: flex;
    height: 90vh;
}

</style>