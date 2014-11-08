define ["jqui", "firebase"], ($jqui, Firebase) ->
  app = () ->
    init = () =>
      this.firebase = new Firebase 'https://conworld.firebaseio.com/forums'
  return app
