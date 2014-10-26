requirejs.config({
    // "enforceDefine": true,
    "paths": {
        "jquery": ["//ajax.googleapis.com/ajax/libs/jquery/2.0.0/jquery.min"],
        "jqui": ["//code.jquery.com/ui/1.11.0/jquery-ui.min"]
    },
    shim: {
        "jqui": {
            export:"$" ,
            deps: ['jquery']
        }
    }
});

requirejs(["jquery", "app"], function ($, app) {
    $(function () {
        app.init();
    });
});
