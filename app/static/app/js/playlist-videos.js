var playlistDownload = (function(){
	var playlist_url = "";
	function downloadAll(e){
		e.preventDefault();
		setTimeout(function(){Materialize.toast('Starting download in a moment :)', 20000, 'rounded')},2000);
		setTimeout(function(){Materialize.toast('Enjoy your videos :)', 20000, 'rounded')},24000);
		$.ajax({
			url : window.location.origin + "/playlist/download/all",
			method : 'GET',
			data : {
				'playlist_url' : playlist_url,
			},
			datatype : 'json',
		})
	}

	function downloadSome(e){
		e.preventDefault();
		var input = $("input[id='mycheckbox']")
		var index_list=[];
		for(var i=0;i<input.length;i++){
			bool_check = input[i].checked;
			if(bool_check){
				index_list.push(i+1)
			} 
		}
		console.log(index_list)
		if(index_list.length ==0){
			Materialize.toast('Please select atleast one video. Thanks :)', 10000, 'rounded');
		}
		else{
			setTimeout(function(){Materialize.toast('Starting download in a moment :)', 20000, 'rounded')},2000);
			setTimeout(function(){Materialize.toast('Enjoy your videos :)', 20000, 'rounded')},24000);
			
		}
		$.ajax({
			url : window.location.origin + "/playlist/download/partial",
			method : 'GET',
			//To send a list through ajax, traditional = true
			traditional: true,
			data : {
				'playlist_url' : playlist_url,
				'index_videos' : index_list,
			},
			datatype : 'json',
			success : function(response){

			}
		})
	}

	function init(){
		query = window.location.search
		for(i=5;i<query.length;i++){
			playlist_url = playlist_url + query[i];
		}
		button_all = document.getElementById('btn-all');
		button_all.addEventListener('click',downloadAll)
		button_some = document.getElementById('btn');
		button_some.addEventListener('click',downloadSome);
	}
	return {
		init: init
	};
})();