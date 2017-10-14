/**
 * @license Copyright (c) 2003-2016, CKSource - Frederico Knabben. All rights reserved.
 * For licensing, see LICENSE.md or http://ckeditor.com/license
 */

CKEDITOR.editorConfig = function( config ) {
	// Define changes to default configuration here.
	// For complete reference see:
	// http://docs.ckeditor.com/#!/api/CKEDITOR.config
	config.extraPlugins = 'wordcount,notification,autosave'; // wordcount plugin
	config.wordcount = {

    // Whether or not you want to show the Paragraphs Count
    showParagraphs: false,

    // Whether or not you want to show the Word Count
    showWordCount: true,

    // Whether or not you want to show the Char Count
    showCharCount: true,

    // Whether or not you want to count Spaces as Chars
    countSpacesAsChars: false,

    // Whether or not to include Html chars in the Char Count
    countHTML: false,
    
    // Maximum allowed Word Count, -1 is default for unlimited
    maxWordCount: -1,

    // Maximum allowed Char Count, -1 is default for unlimited
    maxCharCount: -1,

    // Add filter to add or remove element before counting (see CKEDITOR.htmlParser.filter), Default value : null (no filter)
    filter: new CKEDITOR.htmlParser.filter({
        elements: {
            div: function( element ) {
                if(element.attributes.class == 'mediaembed') {
                    return false;
                }
            }
        }
    })
};

config.autosave = { 
      // Auto save Key - The Default autosavekey can be overridden from the config ...
      Savekey : "autosaveKey",

      // Ignore Content older then X
      //The Default Minutes (Default is 1440 which is one day) after the auto saved content is ignored can be overidden from the config ...
      NotOlderThen : 1440,

      // Save Content on Destroy - Setting to Save content on editor destroy (Default is false) ...
      saveOnDestroy : false,

      // Setting to set the Save button to inform the plugin when the content is saved by the user and doesn't need to be stored temporary ...
      saveDetectionSelectors : "a[href^='javascript:__doPostBack'][id*='Save'],a[id*='Cancel']",

      // Notification Type - Setting to set the if you want to show the "Auto Saved" message, and if yes you can show as Notification or as Message in the Status bar (Default is "notification")
      messageType : "notification",

     // Show in the Status Bar
     //messageType : "statusbar",

     // Show no Message
     //messageType : "no",

     // Delay
     delay : 10,

     // The Default Diff Type for the Compare Dialog, you can choose between "sideBySide" or "inline". Default is "sideBySide"
     diffType : "sideBySide"     
};
	// The toolbar groups arrangement, optimized for two toolbar rows.
	config.toolbarGroups = [
		{ name: 'clipboard',   groups: [ 'clipboard', 'undo' ] },
		{ name: 'editing',     groups: [ 'find', 'selection', 'spellchecker' ] },
		{ name: 'links' },
		{ name: 'insert' },
		{ name: 'forms' },
		{ name: 'tools' },
		{ name: 'document',	   groups: [ 'mode', 'document', 'doctools' ] },
		{ name: 'others' },
		'/',
		{ name: 'basicstyles', groups: [ 'basicstyles', 'cleanup' ] },
		{ name: 'paragraph',   groups: [ 'list', 'indent', 'blocks', 'align', 'bidi' ] },
		{ name: 'styles' },
		{ name: 'colors' },
		{ name: 'about' }
	];
	config.allowedContent = true;

	// Remove some buttons provided by the standard plugins, which are
	// not needed in the Standard(s) toolbar.
	config.removeButtons = 'Underline';

	// Set the most common block elements.
	config.format_tags = 'p;h1;h2;h3;pre';

	// Simplify the dialog windows.
	config.removeDialogTabs = 'image:advanced;link:advanced';
};
