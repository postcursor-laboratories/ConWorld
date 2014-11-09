define ["jqui", "firebase"], ($jqui, Firebase) ->
  htmlEscape = (unsafeString) ->
    div = document.createElement 'div'
    div.appendChild document.createTextNode(unsafeString)
    return div.innerHTML
  doubleQuote = (string) -> "\"#{htmlEscape string}\""
  defineEverything = (@firebaseURL) =>
    @firebase = new Firebase @firebaseURL
    @forums = @firebase.child 'forums'
    @$div = $ '#forums'
    @topic_class_string = 'topic'
    generateTopic = (childSnapshot) =>
      title = childSnapshot.child('title').val()
      description = childSnapshot.child('desc').val()
      $data =
        $ "<div
           id=#{doubleQuote title}
           class=#{doubleQuote @topic_class_string}>
           #{htmlEscape description}
           </div>"
      return $data
    @onTopicAdded = (childSnap, lastName) =>
      @$div.append generateTopic(childSnap)
    @init = =>
      @forums.child('topics').on 'child_added', @onTopicAdded
    return this
  return defineEverything.call {}, 'https://conworld.firebaseio.com/'
