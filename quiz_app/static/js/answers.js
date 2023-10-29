$(document).ready(function() {
    const answer_count = $('#answer-count')
    let answer_nr = 4

    // Add Answer
    const btn_add = $('#add_answer_btn')
    btn_add.click(function(e) {
        e.preventDefault()

        answer_nr++;
        answer_count.val(answer_nr);

        const answersContainer = $('#answers-container')
        answersContainer.append(`
            <div class="form-group" id="answer${answer_nr}-container">
                <label for="answer${answer_nr}">Answer ${answer_nr}:</label>
                <div class="input-group">
                    <div class="input-group-append btn-group-toggle w-100">
                        <input type="text" class="form-control rounded-0" name="answer${answer_nr}" id="answer${answer_nr}">
                        <label class="btn btn-outline-success">
                            <input type="radio" name="is_correct" value="${answer_nr}" autocomplete="off" required> Correct
                        </label>
                    </div>
                </div>
            </div>
        `)
    })

    // Delete answer
    const delete_answer_btn = $('#delete_answer_btn')
    delete_answer_btn.click(function(e) {
        e.preventDefault()

        if(answer_nr >= 3) {
            $(`#answer${answer_nr}-container`).remove()
            answer_nr--;
            answer_count.val(answer_nr);
        }
    })
})