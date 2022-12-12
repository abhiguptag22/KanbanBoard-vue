<template>
  <div class="container mt-5">
    <div class="row">
      <b-nav tabs>
        <b-nav-item-dropdown active id="username" text="Welcome Abhishek Gupta!" toggle-class="nav-link-custom" right>
          <b-dropdown-item @click="logout">Logout</b-dropdown-item>
        </b-nav-item-dropdown>
        <b-nav-item>Summary</b-nav-item>
        <b-nav-item >Export as CSV</b-nav-item>
      </b-nav>
    </div>
    <div class="row mt-5">
      <div>
        <b-button v-b-modal.modal-prevent-closing-2 size="sm" variant="outline-dark">
          <p class="h5 mb-2">
            <b-icon-plus-circle id="addicon" style="width: 26px; height: 28px"></b-icon-plus-circle> Add a new list
          </p>
        </b-button>
        <b-modal id="modal-prevent-closing-2" ref="modal" title="Create a list" @show="resetModal" @hidden="resetModal" @ok="handleOkList">
          <form ref="form" @submit="handleCreateList">
            <b-form-group label="New List" label-for="list-input" invalid-feedback="content is required">
              <b-form-input id="list-input" v-model="newList" required></b-form-input>
            </b-form-group>
          </form>

        </b-modal>
      </div>
    </div>
    <div class="row mt-3">
      <div class="col-3" v-for=" (cards,list) in  allLists" :key="list.key" group="tasks">
        <div class="p-2 alert alert-secondary">
          <div class="d-flex justify-content-between">
            <h3 contenteditable @blur="updateList($event, `${allLists[list].name}`)">{{ allLists[list].name}}</h3>
            <div class="mt-2">
              &nbsp;
              <b-icon-trash @click="removeList" :id="allLists[list].name"></b-icon-trash>
            </div>
          </div>
          <div class="list-group" group="tasks" v-if="allLists[list].name==allLists[0].name">
            <div class="list-group-item text-center">
              <b-button v-b-modal.modal-prevent-closing size="sm">Add a Task</b-button>
              <b-modal id="modal-prevent-closing" ref="modal" title="Create a task" @show="resetModal"
                @hidden="resetModal" @ok="handleOk(`${allLists[0].name}`)">
                <form ref="form">
                  <b-form-group label="Content" label-for="content-input" invalid-feedback="content is required"
                    :state="contentState">
                    <b-form-input id="content-input" v-model="content" :state="contentState" required></b-form-input>
                  </b-form-group>
                  <b-form-group label="Deadline" label-for="deadline-input" invalid-feedback="deadline is required"
                    :state="deadlineState">
                    <b-form-datepicker id="deadline-input" v-model="Deadline" :state="deadlineState" required
                      class="mb-2"></b-form-datepicker>
                  </b-form-group>
                </form>

              </b-modal>
            </div>
          </div>
          <div class="list-group" group="tasks" v-else>
            <div class="list-group-item text-center"></div>
          </div>
          <div class="list-group kanban-column" :list="allLists[list].value" group="tasks">
            <div class="list-group-item" v-for="element in allLists[list].value" :key="element.id">
              <div class="d-flex w-100 justify-content-between">
                <p contenteditable @dragleave="updateContent($event, `${element.id}`)">{{ element.content }}</p>
                <small>
                  <div>
                    <b-dropdown size="sm" id="dropdown-1" text="Actions" class="m-md-2" @hide="resetMoveTo">
                      <b-dropdown-item>Mark as completed</b-dropdown-item>
                      <b-dropdown-item @click.capture.native.stop="moveToHandler">Movo to</b-dropdown-item>
                      <b-dropdown-item @click="removeCard" :id="element.id">Remove</b-dropdown-item>
                      <div v-if="moveToFlag">
                        <b-dropdown-divider ></b-dropdown-divider>
                        <b-dropdown-item v-for="alist in allLists" :key=alist @click="moveACard($event, `${element.id}`)">
                            {{alist.name }}
                        </b-dropdown-item>
                      </div>
                    </b-dropdown>
                  </div>
                </small>
              </div>
              <small>
                <div class="text-muted">Due By - {{ element.deadline }} </div>
              </small>
              <small>
                <div class="text-muted">Created On - {{ element.createdOn }} </div>
              </small>

            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>


<script>
//import draggable
//import draggable from "vuedraggable";
export default {
  name: "Kanban_Dashboard",
  components: {
    //import draggable as a component
  //  draggable
  },
  data() {
    return {
      // for new task
      flaskData: "",
      allLists:"",
      newTask: "",
      newList:"",
      editedCard: "",
      content: "",
      Deadline: "",
      cardId: "",
      deadlineState: null,
      contentState: null,
      taskLists:['todo', 'doing'],
      moveToFlag:false,
      access_token : ""
    };
  },
  methods: {
    async moveACard(event, cardid) {
      console.log(event.target.text)
      console.log(cardid)
      await fetch(`http://localhost:5000/movecard/${cardid}/${event.target.text}`, {method:"POST"})

      const cResponse = await fetch(`http://localhost:5000/allData/${localStorage.getItem('current_user_id')}`)
        const cObject = await cResponse.json()
        this.allLists = cObject
    },
    moveToHandler() {
      this.moveToFlag=true;
    },
    resetMoveTo() {
      this.moveToFlag=false;
    },
    async removeList(event) {
      console.log(event.target.id)
      await fetch("http://localhost:5000/removelist/" + event.target.id)

      const cResponse = await fetch(`http://localhost:5000/allData/${localStorage.getItem('current_user_id')}`)
        const cObject = await cResponse.json()
        this.allLists = cObject
  
    },

    async removeCard(event) {
      console.log(event.target.id)
      await fetch("http://localhost:5000/removecard/" + event.target.id)

      const cResponse = await fetch(`http://localhost:5000/allData/${localStorage.getItem('current_user_id')}`)
        const cObject = await cResponse.json()
        this.allLists = cObject
  
    },
    async updateContent(event, key) {
      await fetch(`http://localhost:5000/editcard/${key}`, {
        method: "POST",
        body: JSON.stringify({
          newContent: event.target.innerText
        }),
        headers: {
          "Content-type": "application/json; charset-UTF-8"
        }
      })

    },
    async updateList(event, key) {
      await fetch(`http://localhost:5000/editlist/${key}`, {
        method: "POST",
        body: JSON.stringify({
          newListName : event.target.innerText
        }),
        headers: {
          "Content-type": "application/json; charset-UTF-8"
        }
      })

    },
    
    async handleCreateList() {
      this.$bvModal.hide('modal-prevent-closing-2')

      if (this.newList) {
        await fetch(`http://localhost:5000/lists`, {
        method: "POST",
        body: JSON.stringify({
          newList : this.newList,
          current_user_id : localStorage.getItem('current_user_id')
        }),
        headers: {
          "Content-type": "application/json; charset-UTF-8"
        }
      })
      const cResponse = await fetch(`http://localhost:5000/allData/${localStorage.getItem('current_user_id')}`)
        const cObject = await cResponse.json()
        this.allLists = cObject
      }

    },
    handleOkList() {
      this.handleCreateList()
    },

    resetModal() {
      this.content = ""
      this.Deadline = ""
      this.newList=""
    },
    handleOk(parent) {
      this.handleSubmit(parent)
    },
    async handleSubmit(parent) {
      this.$nextTick(async () => {
        this.$bvModal.hide('modal-prevent-closing')
        const postCard = await fetch("http://localhost:5000/tasks", {
          method: "POST",
          body: JSON.stringify({
            content: this.content,
            deadline: this.Deadline,
            taskParent: parent,
            current_user_id: localStorage.getItem('current_user_id')
          }),
          headers: {
            "Content-type": "application/json; charset-UTF-8"
          }
        })
        const obj = await postCard.json()
        console.log(obj)


        const cResponse = await fetch(`http://localhost:5000/allData/${localStorage.getItem('current_user_id')}`)
        const cObject = await cResponse.json()
        this.allLists = cObject
      })
    },
    logout() {
      this.$router.push({name:'logout'})
    }
  },
  mounted: async function () {
    const cResponse = await fetch(`http://localhost:5000/allData/${localStorage.getItem('current_user_id')}`,{
      headers: {
        "Authentication-Token":localStorage.getItem('access_token')
      }
    }

)
    const cObject = await cResponse.json()
    this.allLists = cObject
    this.access_token = localStorage.getItem("access_token")
    
  },
  beforeCreate: function() {
    if (!localStorage.getItem('access_token')) {
      this.$router.push({name:'login'})
    }
  }
};
</script>





<style>
/* light stylings for the kanban columns */
.kanban-column {
  min-height: 300px;
}

#addicon {
  width: 3%;
}

.list-group-item {
  min-block-size: 49px;
}

</style>