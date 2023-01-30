/* Javascript for CollapsibleXBlock. */
function AddCollapsibleXBlock(runtime, element, block_element, init_args) {
  return new CollapsibleXBlock(runtime, element, init_args);
}

function CollapsibleXBlock(runtime, element, init_args) {
    $(document).ready(function edit_to_submit() {
        $('#header_edit_btn').click(function() {
            $(this).val('Submit');
        });
     });

    $(document).ready(function textfield() {
        $('#header_edit_btn').click(function textfield_appearance() {
            $('#header_edit_btn').after('<input type="text" id="textInput" placeholder = "enter_new_header" value="">');

//            if ($('#header_edit_btn').val == 'Submit') {
//               $('#header_edit_btn').click(function get_input_data() {
//                    pass;
//               });
//            };
        });

        $('#reset').click(function reset_textfield() {
            $('#textInput').val("");
            $('text').val('');
        });

        $(document).ready(function textfield_options() {
            $('#header_edit_btn').click(function() {
                $('#header_btn').val($('textInput').val(''));
            });
        });

        $(document).on('click', '#accordion #header_edit_btn', function(){
            let editable = $(this).prev('.header_btn').attr('contenteditable');
            if(editable) {
                $(this).text('Edit');
                $('.header_btn').css({'border': ''});
                $(this).prev('.header_btn').removeAttr('contenteditable');
            }
            else{
                $(this).text('Save')
                $('.header_btn').css({'border': '1px solid'});
                $(this).prev('.header_btn').attr('contenteditable', 'true');
            }
        })
    });

    function editHeader(new_header_name) {
        $('.header_edit_btn', element).text(new_header_name.new_header_name);
    }

    var handlerUrl = runtime.handlerUrl(element, 'edit_header');

    $('.header_edit_btn', element).click(function(eventObject) {
        $.ajax({
            type: "POST",
            url: handlerUrl,
            data: JSON.stringify({header_name: new_header_name}),
            success: editHeader
        });
    });
    return {};
 };
//
//function ThumbsAside(runtime, element, block_element, init_args) {
//    return new ThumbsBlock(runtime, element, init_args);
//
//function ThumbsBlock(runtime, element, init_args) {
//    function updateVotes(votes) {
//        $('.upvote .count', element).text(votes.up);
//        $('.downvote .count', element).text(votes.down);
//    }
//
//    var handlerUrl = runtime.handlerUrl(element, 'vote');
//
//    $('.upvote', element).click(function(eventObject) {
//        $.ajax({
//            type: "POST",
//            url: handlerUrl,
//            data: JSON.stringify({voteType: 'up'}),
//            success: updateVotes
//        });
//    });
//
//    $('.downvote', element).click(function(eventObject) {
//        $.ajax({
//            type: "POST",
//            url: handlerUrl,
//            data: JSON.stringify({voteType: 'down'}),
//            success: updateVotes
//        });
//    });
//
//    return {};
//};
