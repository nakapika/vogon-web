angular.module('annotationApp').factory('selectionService', ['appellationService', function(appellationService) {
    var service = {
        // Word callback hoppers.
        word_success_callbacks: [],
        word_failure_callbacks: [],

        // Appellation callback hoppers.
        appellation_success_callbacks: [],
        appellation_failure_callbacks: [],

        // Current selection. Holds {jQuery} objects.
        selected_words: $(),
        selected_appellation: null,
    }

    /**
      * Indicates whether/not we are now in the process of selecting words.
      */
    service.wordsAreSelected = function() {
        return (service.selected_words.length > 0);
    }

    /**
      * Unselect all words.
      */
    service.resetWordSelection = function() {
        service.selected_words.removeClass("selected");
        service.selected_words = $();
    }

    /**
      * Unselect all appellations.
      *
      * This is kind of weird at the moment, since we only select one
      *  appellation at a time.
      */
    service.resetAppellationSelection = function() {
        service.selected_appellation = null;
    }

    /**
      *  Clear word callback hoppers.
      */
    service.resetWordCallbacks = function() {
        service.word_success_callbacks = [];
        service.word_failure_callbacks = [];
    }

    /**
      *  Clear appellation callback hoppers.
      */
    service.resetAppellationCallbacks = function() {
        service.appellation_success_callbacks = [];
        service.appellation_failure_callbacks = [];
    }

    /**
      *  Handle the failure to select a word.
      */
    service.failWordExpectation = function() {
        service.word_failure_callbacks.forEach(function(callback) {
            callback();
        });
        service.resetWordCallbacks();
        service.resetWordSelection();
        service.resetAppellationSelection();
    }

    /**
      *  Handle successful word selection.
      */
    service.succeedWordExpectation = function() {
        service.word_success_callbacks.forEach(function(callback) {
            callback(service.selected_words);
        });

        if (service.autorelease) service.releaseWords();
        service.failAppellationExpectation();
    }

    /**
      *  Handle the failure to select an appellation.
      */
    service.failAppellationExpectation = function() {
        service.appellation_failure_callbacks.forEach(function(callback) {
            callback();
        });
        service.resetAppellationCallbacks();
        service.resetAppellationSelection();
    }

    /**
      *  Handle successful appellation selection.
      */
    service.succeedAppellationExpectation = function() {
        service.appellation_success_callbacks.forEach(function(callback) {
            callback(service.selected_appellation);
        });
        if (service.autorelease) service.resetAppellationCallbacks();
        service.failWordExpectation();
    }

    /**
      *  Discriminates between words that are and are not part of appellations.
      *  @param {jQuery} word - A jQuery-selected <word> object.
      */
    service.isAppellation = function(word) {
        if (word.is('.appellation')) return true;
        return false;
    }

    /**
      *  Retrieves the appellation ID from a jQuery-selected <word> element.
      *  @param {jQuery} word - A jQuery-selected <word> object.
      */
    service.getAppellationID = function(word) {
        if (service.isAppellation) return word.attr('appellation');
    }

    /**
      *  Register success and failure callbacks for word selection events.
      *  @param {function} success_callback - Function to be called when the user selects a word.
      *  @param {function} failure_callback - Function to be called when the user fails to select a word.
      *  @param {bool} autorelease - If false, word selection will not be released until service.releaseWords() is called.
      */
    service.expectWords = function(success_callback, failure_callback, autorelease) {
        if (success_callback) service.word_success_callbacks.push(success_callback);
        if (failure_callback) service.word_failure_callbacks.push(failure_callback);
        console.log(autorelease);
        service.autorelease = autorelease;
    }

    service.releaseWords = function() {
        service.resetWordSelection();
    }

    service.releaseAppellations = function() {
        service.resetAppellationCallbacks();
    }

    /**
      *  Register success and failure callbacks for appellation selection events.
      *  @param {function} success_callback - Function to be called when the user selects an appellation.
      *  @param {function} failure_callback - Function to be called when the user fails to select an appellation.
      */
    service.expectAppellation = function(success_callback, failure_callback) {
        if (success_callback) service.appellation_success_callbacks.push(success_callback);
        if (failure_callback) service.appellation_failure_callbacks.push(failure_callback);
    }

    /**
      *  Callback for <word> click event.
      *  @param {jQuery.Event} event - Click event with a valid ``target``.
      */
    service.handleClick = function(event) {

        var word = $(event.target);
        // If the word is part of an appellation, select it (and succeed).
        if (service.isAppellation(word)) {
            service.handleSelectAppellation(event);

        // If the word is not part of an Appellation, add word to the word
        //  selection hopper.
        } else {
            if (service.selected_words.length > 0 & event.shiftKey) {
                // $.add() does not modify in-place.
                service.extendWordSelection(word);
                // service.selected_words = service.selected_words.add(word);
            } else {
                service.replaceWordSelection(word);
            }
            service.selected_words.addClass("selected");
            service.selectedWordPopover();
        }
    }

    service.replaceWordSelection = function(word) {
        service.resetWordSelection();
        service.selected_words = word;
    }


    /**
      * Display a popover with button on the last selected word.
      */
    service.selectedWordPopover = function() {
        var lastId = service.selected_words[service.selected_words.length - 1].id;
        $('word').popover('destroy');
        $('word#' + lastId).popover({
            html: true,
            template: '<div class="popover" role="tooltip"><div class="arrow"></div><h3 class="popover-title"></h3><div class="popover-content popover-action"></div></div>',
            content:'<a class="btn btn-xs btn-primary glyphicon glyphicon-plus" id="wordPopoverOK"></a>'
        });
        $('word#' + lastId).popover('show');
        $('#wordPopoverOK').on('click', function() {
            $('word').popover('destroy');
            service.handleSelectWord();
        });
    }

    /**
      *  Callback for select word event.
      *  @param {jQuery.Event} event
      */
    service.handleSelectWord = function(event) {
        service.succeedWordExpectation();
    }

    /**
      *  Callback for select appellation event.
      *  @param {jQuery.Event} event
      */
    service.handleSelectAppellation = function(event) {
        var word = $(event.target);
        service.selected_appellation = appellationService.getAppellation(service.getAppellationID(word));
        service.succeedAppellationExpectation();
    }

    /**
      * Handles the event that user presses the enter key on their keyboard.
      */
    service.handleEnter = function(event) {
        if (service.wordsAreSelected()) service.handleSelectWord(event);
    }

    /**
      *  Callback for ESC key event.
      */
    service.handleEsc = function(event) {
        service.releaseWords();
    }

    /**
      * Select all elements from start through end.
      * @param {jQuery} start - The starting element.
      * @param {jQuery} end - The ending element.
      */
    service.selectIntermediateWords = function(start, end) {
        // Select words between start and end. If start, end, or any
        // intermediate words are appellations, abort and clear all selections.
        var toSelect = start.nextUntil(end).add(start).add(end);

        if (toSelect.is('.appellation')) {
            // Selection crosses an appellation. Abort!
            return false;
        }

        // Otherwise, select everything.
        service.selected_words = service.selected_words.add(toSelect);
        return true;
    }

    /**
      * Extend the current selection of words to the target word, including all intermediate words.
      * @param {jQuery} target - The word element to which the current selection should be extended.
      */
    service.extendWordSelection = function(target) {
        // User can select multiple non-appellation words by holding
        //  the shift key.
        var first = service.selected_words.first();
        var last = service.selected_words.last();
        var index_target = $('word').index(target);
        var index_first = $('word').index(first);
        var index_last = $('word').index(last);
        var inter;

        // Select words between the new target word and either the
        //  start or end of the current selection.
        if (index_target < index_first) {       // Target is earlier.
            inter = service.selectIntermediateWords(target, first);
            targetElement = last;
        } else if (index_last < index_target) {     // Target is later.
            inter = service.selectIntermediateWords(last, target);
            targetElement = target;
        }

        // If multi-selection was aborted, the `targetElement` (where the icons)
        //  should appear should be the last element clicked (`target`).
        if (!inter){
            service.replaceWordSelection(target);
        }
    }

    service.bindWords = function() {
        $('word').click(service.handleClick);

        $(document).keypress(function(event) {
            if(event.which == 13) service.handleEnter(event);
            if(event.which == 27) service.handleEsc(event);
        });
    }
    service.bindWords();
    return service;
}]);