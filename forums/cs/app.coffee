define ["jqui", "firebase"], ($jqui, Firebase) ->
  class App
    constructor: (@firebase) ->
      @forums = new Firebase "#{@firebase}/forums"
    @$div = $ '#forums'
    @onForumAdded: (childSnap, lastName) ->
      @$div.append childSnap
    init: ->
      @firebase.on 'child_added', onForumAdded
      
  return app
