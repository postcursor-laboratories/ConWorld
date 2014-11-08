requirejs.config
  paths:
    jquery:
      ["//ajax.googleapis.com/ajax/libs/jquery/2.0.0/jquery.min"]
    jqui:
      ["//code.jquery.com/ui/1.11.0/jquery-ui.min"]
    firebase:
      ["https://cdn.firebase.com/js/client/1.1.2/firebase"]
  shim:
    jqui:
      exports:
        "$"
      deps:
        ['jquery']
    firebase:
      exports:
        "Firebase"

requirejs ["jquery", "app"], ($, app) -> $ app.init
