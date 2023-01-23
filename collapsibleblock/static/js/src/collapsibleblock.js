/* Javascript for CollapsibleXBlock. */
function AddCollapsibleXBlock(runtime, element, block_element, init_args) {
  return new CollapsibleXBlock(runtime, element, init_args);
}

function CollapsibleXBlock(runtime, element, init_args) {
    $(document).ready(function() {
        $('#header_edit_btn').click(function() {
            $(this).val('Submit');
        });
     });

    $(document).ready(function() {
        $('#header_edit_btn').click(function() {
            $('#header_edit_btn').after('<input type="text" id="textInput" value="">');
        });
    });
//    function editHeader(new_header_name) {
//        $('.header_edit_btn', element).text(new_header_name.new_header_name);
//    }

//    var handlerUrl = runtime.handlerUrl(element, 'edit_header');

//    $('.header_edit_btn', element).click(function(eventObject) {
//        $.ajax({
//            type: "POST",
//            url: handlerUrl,
//            data: JSON.stringify({header_name: new_header_name}),
//            success: editHeader
//        });
//    });
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
