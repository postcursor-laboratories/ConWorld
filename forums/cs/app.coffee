define ["jqui", "firebase"], ($jqui, Firebase) ->
  doubleQuote = (string) -> "\"#{string}\""
  htmlEscape = (unsafeString) ->
    div = document.createElement 'div'
    div.appendChild document.createTextNode(unsafeString)
    return div.innerHTML
  class App
    constructor: (@firebase) ->
      @forums = new Firebase "#{@firebase}/forums"
    @$div = $ '#forums'
    @topic_class_string = 'topic'
    generateTopic = (childSnapshot) ->
      title = childSnapshot.child('title').val()
      description = childSnapshot.child('desc').val()
      $data =
        $ "<div
           id=#{doubleQuote title}
           class=#{doubleQuote @topic_class_string}>
           #{htmlEscape desc}
           </div>"
      return $data
    @onTopicAdded: (childSnap, lastName) ->
      @$div.append generateTopic(childSnap)
    init: ->
      @firebase.child('topics').on 'child_added', onTopicAdded
  return app
