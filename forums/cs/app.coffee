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
  htmlSafeId = (id) -> id.replace(/[^a-zA-Z0-9]/, '_')
  defineEverything = (@firebaseURL) =>
    @firebase = new Firebase @firebaseURL
    @forums = @firebase.child 'forums'
    @$div = $ '#forums'
    @topic_class_string = 'topic'
    @desc_class_string = 'topic-description'
    generateTopic = (childSnapshot, callback) =>
      title = childSnapshot.child('title').val()
      description = childSnapshot.child('desc').val()
      await limitedHtmlEscape description, defer descEscaped
      $data =
        $ "<div
           id=#{doubleQuote htmlSafeId title}
           class=#{doubleQuote htmlSafeId @topic_class_string}>
             <p class=#{doubleQuote htmlSafeId @desc_class_string}>
               #{descEscaped}
             </p>
           </div>"
      callback $data
    secureOTA = (childSnap, lastName) =>
      await generateTopic childSnap, defer generatedDiv
      console.log(generatedDiv)
      @$div.append generatedDiv
    @onTopicAdded = (childSnap, lastName) ->
      secureOTA.apply this, arguments
    secureInit = =>
      @forums.child('topics').on 'child_added', @onTopicAdded
    @init = ->
      secureInit.apply this, arguments
    return this
  return defineEverything.call {}, 'https://conworld.firebaseio.com/'
