jQuery(function(){
    var chat = jQuery('<div id="chat"></div>')
    chat.css(
        { "position": "fixed"
        , "bottom": "4px"
        , "right": "4px"
        , "border": "1px solid #444"
        , "background": "#eee"
        }
    )

    var header = jQuery('<div id="chat_header">Header</div>')
    header.appendTo(chat)
    header.css(
        { "border-bottom": "1px solid #888"
        , "font-size": "110%"
        , "padding": "4px"
        }
    )

    var log = jQuery('<div id="chat_log"></div>')
    log.appendTo(chat)
    log.css(
        { "padding-left": "4px"
        , "margin-top": "4px"
        , "margin-bottom": "4px"
        , "overflow-y": "scroll"
        , "height": "8em"
        , "min-height": "8em"
        }
    )
    var scrollLog = function(force){
        var l = log[0]
        l.scrollTop = l.scrollHeight
        // FIXME: inhibit autoscroll
    }

    var form = jQuery('<div id="chat_form"></div>')
    form.css(
        { "border-top": "1px solid #888"
        , "padding": "4px"
        }
    )
    form.appendTo(chat)

    var input = jQuery('<input id="chat_input" placeholder="Type here"/>')
    input.appendTo(form)
    input.keypress(function(e){
        if (e.charCode === 13) {
            jQuery("#chat_send").click()
            return false
        }
    })

    var send = jQuery('<button id="chat_send">Send</button>')
    send.appendTo(form)
    send.click(function(){
        var text = input.val().trim()
        if (!text) { return false }

        input.val('')
        jQuery
            .post("{% url 'chat:send' %}",
                { 'text': text
                , 'title': document.title
                , 'path': document.location.pathname
                {% if user.is_staff %}
                , 'cid': '{{ CHAT_ID|escapejs }}'
                {% endif %}
                }
            )
            .done(function(data){
                var entry = jQuery('<div></div>')
                entry.html(data)
                entry.appendTo(log)
                scrollLog("force")
            })
            .fail(function(e){
                console.error('error sending text, try again.')
                input.val(text)
            }).always(function(){
                input.focus()
            })
    })

    var firstPull = true
    var pullTimer = null // TODO: inhibit autoscroll
    var pull = function(){
        jQuery
            .get("{{ MEDIA_URL }}/sepiida_chat/{{ CHAT_ID }}.html")
            .done(function(data) {
                log.html(data)
                scrollLog()
            })
            .fail(function(e){
                log.html('Privet!')
            })
            .always(function(){
                if (firstPull) {
                    chat.appendTo(jQuery("body"))
                    scrollLog("force")
                    firstPull = false
                }
                pullTimer = setTimeout(pull, 1000)
            })
    }
    pull()
})
