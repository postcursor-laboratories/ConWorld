define(["jqui", "firebase"], function ($undef, Firebase) {
    var app = {};
    
    var hooks = {};
    app.hooks = hooks;
    function render(regularContent) {
        
    }
    function add_post_method($area) {
        return function add_post_callback(idSnap) {
            var uniqueID = idSnap.key();
            var postid = idSnap.val();
            var post = app.fire.child('posts').child(postid.toString());
            var postExists = post.exists();
            var name = post.key();
            var renderedContent = post.child('content/rendered').val();
            function isRendered() {
                return renderedContent !== null;
            }
            if (!isRendered()) {
                renderedContent = render(post.child('content/regular').val());
            }
        };
    }
    function add_posts(posts, $area) {
        posts.forEach(add_post_method($area));
    }
    function add_mod_method($area) {
        return function add_mod_callback(post) {
            
        };
    }
    function add_modrs(modrs, $area) {
        modrs.forEach(add_mod_method($area));
    }
    function generate_forum_topic(topic) {
        var fb = app.fire;
        var stiky = topic.child('sticky-posts');
        var posts = topic.child('posts');
        var modrs = topic.child('moderators');
        var $container = $('<div id="' + topic.name() + '" class="forum-topic"></div>');
        var $stickyposts = $('<div class="posts sticky-posts"></div>');
        var $posts = $('<div class="posts"></div>');
        var $mods = $('<div class="moderator-list"></div>');
        add_posts(posts, $posts);
        add_posts(stiky, $stickyposts);
        add_modrs(modrs, $mods);
        $container.append($stickyposts);
        $container.append($posts);
        $container.append('<div class="TODO">TODO: make mods have seperator here</div>');
        $container.append($mods);
        return $container;
    }
    hooks.add_forum = function (forum, lastForumName) {
        var name = forum.key();
        var fcontainer = $('#forums');
        var topic = generate_forum_topic(forum);
        if (!lastForumName) {
            // just dump it at the top
            fcontainer.prepend(topic);
        } else {
            $(topic).insertAfter('#' + lastForumName);
        }
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
