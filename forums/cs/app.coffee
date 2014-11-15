define ["jqui", "firebase"], ($jqui, Firebase) ->
  htmlEscape = (unsafeString) ->
    div = document.createElement 'div'
    div.appendChild document.createTextNode(unsafeString)
    return div.innerHTML
  limitedHtmlEscapeURL = 'escapelimited.py'
  limitedHtmlEscape = (unsafeString, callback) ->
    await $.post limitedHtmlEscapeURL, {'input': unsafeString}, defer output
    callback output
  doubleQuote = (string) -> "\"#{htmlEscape string}\""
  defineEverything = (@firebaseURL) =>
    @firebase = new Firebase @firebaseURL
    @forums = @firebase.child 'forums'
    @$div = $ '#forums'
    @topic_class_string = 'topic'
    @desc_class_string = 'topic-description'
    generateTopic = (childSnapshot) =>
      title = childSnapshot.child('title').val()
      description = childSnapshot.child('desc').val()
      await limitedHtmlEscape description, defer descEscaped
      $data =
        $ "<div
           id=#{doubleQuote title}
           class=#{doubleQuote @topic_class_string}>
             <p class=#{doubleQuote @desc_class_string}>
               #{descEscaped}
             </p>
           </div>"
      return $data
    secureOTA = (childSnap, lastName) =>
      @$div.append generateTopic(childSnap)
    @onTopicAdded = (childSnap, lastName) ->
      secureOTA.apply this, arguments
    secureInit = =>
      @forums.child('topics').on 'child_added', @onTopicAdded
    @init = ->
      secureInit.apply this, arguments
    return this
  return defineEverything.call {}, 'https://conworld.firebaseio.com/'
