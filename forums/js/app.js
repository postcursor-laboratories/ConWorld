define(["jqui", "firebase"], function ($undef, Firebase) {
    var app = {};
    
    app.init = function init() {
        app.fire = new Firebase("https://conworld.firebaseio.com").child("forums");
        console.log('initalized forums');
    };

    return app;
});
