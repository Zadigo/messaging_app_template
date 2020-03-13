var apicall = function(method, url, data) {
    var request = new XMLHttpRequest()

    request.responseType = "json"
    request.open(method, url, true)
    request.onload = function() {
        return request.response
    }
    request.send()
}

var messagingbox = {
    template: "\
    <transition name='reported_thread'>\
        <div v-if='!threadreported' class='row'>\
            <div class='col s12 m12 l12'>\
                <textarea v-model='messagebox.message' name='message' id='message-textbox' cols='30' rows='100'></textarea>\
                <button @click='createnewmessage' class='btn-large'>New message</button>\
            </div>\
        </div>\
        <div v-else class='thread-reported'>\
            The thread has been blocked. No messages cannot be posted until admin verficiation.\
        </div>\
    </transition>\
    ",
    data() {
        return {
            threadreported: false,
            messagebox: {message: ""}
        }
    },
    methods: {
        createnewmessage: function() {
            var self = this
            var copiedmessage = {...this.$data.messagebox}

            $.ajax({
                type: "POST",
                url: "/api/v1/thread/926421b429/new-message",
                data: copiedmessage,
                dataType: "json",
                success: function (response) {
                    self.$data.messagebox.message = ""
                    self.$emit('createnewmessage', copiedmessage)
                },
                error: function(response) {
                    copiedmessage["message"] = "An error occured while attempting to send your message"
                }
            });
        },

    }
}

var mymessages = {
    props: ["messages"],
    template: "\
    <section class='section forum'>\
        <div class='row'>\
            <div class='col s12 m6 l6'>\
                <div class='btn white black-text'><i class='material-icons'>refresh</i></div>\
                <div @click='reportthread' class='btn white black-text'><i class='material-icons'>block</i></div>\
            </div>\
        </div>\
        <div class='row'>\
            <div class='col s12 m12 l12'>\
                <div class='windows'>\
                    <div class='threads-window'>\
                        <div class='thread'>I am a thread</div>\
                    </div>\
                    <div class='messages-window'>\
                        <div v-for='message in messages' :key='message.id' class='message'>\
                            {{ message.message}}\
                            <i @click='deletemessage(message)' class='material-icons'>delete</i>\
                        </div>\
                    </div>\
                </div>\
            </div>\
        </div>\
        <transition name='reported_thread'>\
            <div v-show='!threadreported' class='row'>\
                <div class='col s12 m12 l12'>\
                    <textarea v-model='messagebox.message' name='message' id='message-textbox' cols='30' rows='100'></textarea>\
                    <button @click='createnewmessage' class='btn-large'>New message</button>\
                </div>\
            </div>\
        </transition>\
    </section>\
    ",
    data() {
        return {
            threadreported: false,
            messagebox: {message: "", mark_as_delete: false}
        }
    },
    mounted() {
        // In order to be able to delete messages
        // that were created with Vue, we need to
        // add the other keys for the app not to
        // break when deleting for example
        var d = new Date()

        this.$data.messagebox.created_on = d.getFullYear() + "-" + d.getMonth() + "-" + d.getDay()
    },
    methods: {
        createnewmessage: function() {
            var self = this
            var copiedmessage = {...this.$data.messagebox}

            $.ajax({
                type: "POST",
                url: "/api/v1/thread/926421b429/new-message",
                data: copiedmessage,
                dataType: "json",
                success: function (response) {
                    self.$data.messagebox.message = ""
                    response["mark_as_delete"] = false
                    self.$emit('createnewmessage', response)
                },
                error: function(response) {
                    copiedmessage["message"] = "An error occured while attempting to send your message"
                }
            });
        },
        deletemessage: function(message) {
            $.ajax({
                type: "POST",
                url: "/api/v1/thread/926421b429/delete-message",
                data: {id: message.id, thread_reference: message.thread_reference.reference},
                dataType: "json",
                success: function (response) {
                    message.mark_as_delete = true
                }
            });
        },
        reportthread: function() {
            this.$data.threadreported = true
            // $.ajax({
            //     type: "POST",
            //     url: "/api/v1/thread/926421b429/report",
            //     data: {"reason": ""},
            //     dataType: "json",
            //     success: function (response) {
                    
            //     }
            // });
        }
    }
}

var messagesapp = new Vue({
    el: "#messagesapp",
    components: {mymessages},
    data() {
        return {
            currentthread: "",
            messages: []
        }
    },
    computed: {
        messagelist() {
            return this.$data.messages.filter(message => {
                return message.mark_as_delete === false
            })
        }
    },
    mounted() {
        var self = this
        var response = apicall("GET", "/api/v1/threads")
        // console.log(response)
        $.ajax({
            type: "GET",
            url: "/api/v1/thread/926421b429",
            dataType: "json",
            success: function (response) {
                response.forEach(message => {
                    message['mark_as_delete'] = false
                })
                self.$data.messages = response
            }
        });
    },
    methods: {
        showcreatedmessage: function(message) {
            this.$data.messages.push(message)
        } 
    }
})