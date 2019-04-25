
    function init() {
      //// Initialize Firebase.
      //// TODO: replace with your Firebase project configuration.
      var config = {
      
      };
      firebase.initializeApp(config);

      //// Get Firebase Database reference.
      var firepadRef = getExampleRef();

      //// Create CodeMirror (with lineWrapping on).
      var editor = ace.edit("firepad-container");
      editor.setTheme("ace/theme/textmate");
      var session = editor.getSession();
      session.setUseWrapMode(true);
      session.setUseWorker(false);
      session.setMode("ace/mode/tex");

      //// Create Firepad (with rich text toolbar and shortcuts enabled).
      // var firepad = Firepad.fromCodeMirror(firepadRef, codeMirror,
      //     { richTextToolbar: true, richTextShortcuts: true });

      //// Initialize contents.
      var firepad = Firepad.fromACE(firepadRef, editor, {
        defaultText: '{{ instance.content }}'
      });
    }

    // Helper to get hash from end of URL or generate a random one.
    function getExampleRef() {
      var ref = firebase.database().ref();
      var hash = window.location.hash.replace(/#/g, '');
      if (hash) {
        ref = ref.child(hash);
      } else {
        ref = ref.push(); // generate unique location.
        window.location = window.location + '#' + ref.key; // add it as a hash to the URL.
      }
      if (typeof console !== 'undefined') {
        console.log('Firebase data: ', ref.toString());
      }
      return ref;
    }
