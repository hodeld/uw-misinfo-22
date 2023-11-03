$(document).ready(function () {
    setMsgTimeout(mainMsgId);
});

const mainMsgId = '#id_up_message';

function setMsgTimeout(msgId){
    setTimeout(function () {
            $(msgId).children().last().remove();  // as already an element could be deleted -> delete last one
        }, 5 * 1000);

}