define ["jqui", "firebase"], ($jqui, Firebase) ->
  doubleQuote = (string) -> "\"#{string}\""
  htmlEscape = (unsafeString) ->
    div = document.createElement 'div'
    div.appendChild document.createTextNode(unsafeString)
    return div.innerHTML
  class App
    constructor: (@firebaseURL) ->
      @firebase = new Firebase @firebaseURL
      @forums = @firebase.child 'forums'
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
    oTA = @onTopicAdded
    init: ->
      console.log this
      @forums.child('topics').on 'child_added', oTA
  return new App("conworld.firebaseio.com")
