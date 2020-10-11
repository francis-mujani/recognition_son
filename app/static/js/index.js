
function submit_message() {

    fetch(`${window.origin}/fitmusic`, {
        method: "POST",
        credentials: "include",
        cache: "no-cache",
        headers: new Headers({
        "content-type": "application/json"
        })
    })
        .then(function (response) {
        if (response.status !== 200) {
            console.log(`Il y'a un probleme de status: ${response.status}`);
            return;
        }
        response.json().then(function (data) {
            if (data['error']) {
                $('#errorAlert').text(data['error']).show();
                $('#successAlert').hide();
            }
            else {
                $('#successAlert').text(data['SONG_NAME']).show();
                $('#errorAlert').hide();
            }
        });
        })
        .catch(function (error) {
        console.log("Fetch error: " + error);
        })

}