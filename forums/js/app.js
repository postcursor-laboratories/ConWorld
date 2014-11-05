define(["jqui", "firebase"], function ($undef, Firebase) {
    var app = {};
    
    var hooks = {};
    app.hooks = hooks;
    function generate_forum_topic(topic) {
        var fb = app.fire;
        var stiky = topic.child('sticky-posts');
        var posts = topic.child('posts');
        var $container = $($('<div id="' + topic.name() + '" class="forum-topic"></div>'));
        console.log($container);
        return $container;
    }
    hooks.add_forum = function (forum, lastForumName) {
        var name = forum.name();
        var fcontainer = $('#forums');
        var topic = generate_forum_topic(forum);
        if (!lastForumName) {
            // just dump it at the top
            fcontainer.prepend(topic);
        } else {
            $(topic).insertAfter('#' + name);
        }
        console.log('added ' + name + ' as ' + topic);
    };

    function setup_firehooks(fb) {
        fb.child('topics').on('child_added', hooks.add_forum);
    }

    app.init = function init() {
        app.fire = new Firebase("https://conworld.firebaseio.com").child("forums");
        setup_firehooks(app.fire);
        console.log('initalized forums');
    };

    return app;
});
