var playlist = (function(){

	function createConfirmPlaylistCard(title,author,views,videos_count,playlist_image){
		existing_card = document.getElementById('playlist_card')
		if (existing_card !== null){
			existing_card.parentNode.removeChild(existing_card);
		}
		card = document.createElement('div');
		card.innerHTML = '<div class="row" ><div class="col s12 m6 l4 offset-l4 offset-m3"><div class="card"><div class="card-image"><img id ="playlist_image" src= ""></div><div class="card-content"><p id="title" style="font-size:20px"></p><p id="author" style="font-size:20px"></p><p id="videos_count" style="font-size:20px"></p><p id="views" style="font-size:20px"></p></div><div class="card-action" style="text-align:center"><a id="pl-true" href="" style="color:#22BCE7">Confirm playlist</a><a id="pl-false" href="" style="color:#22BCE7">Not my playlist</a></div></div></div></div>';
		card.style.marginTop = "5%";
		document.body.appendChild(card);
		card.id = "playlist_card"
		card_image = document.getElementById('playlist_image');
		card_image.src = playlist_image;
		playlist_title = document.getElementById('title');
		playlist_title.innerHTML = title;
		playlist_author = document.getElementById('author')
		playlist_author.innerHTML = "By: " + author;
		playlist_views = document.getElementById('views')
		playlist_views.innerHTML = "YouTube Views: " + views;
		playlist_videos_count = document.getElementById('videos_count')
		playlist_videos_count.innerHTML = "Videos: " + videos_count;
		playlist_search = document.getElementById('icon_prefix');
		playlist_url = playlist_search.value;
		pl_true = document.getElementById('pl-true')
		pl_true.href = window.location.origin + "/playlist/download/?url=" + playlist_url;
	}

	function confirmPlaylist(e){
		e.preventDefault();
		playlist_search = document.getElementById('icon_prefix');
		playlist_url = playlist_search.value;
		$.ajax({
			url : window.location.origin+'/playlist/confirm',
			method : 'GET',
			data : {
				'playlist_url' : playlist_url, 
			},
			datatype : 'json',
			success : function(response){
				var title = response.title;
				var author = response.author;
				var views = response.views;
				var videos_count = response.videos_count;
				var playlist_image = response.playlist_image;
				createConfirmPlaylistCard(title,author,views,videos_count,playlist_image);
			}
		})
	}

	function confirmPlaylist2(e){
		e.preventDefault();
		if (e.keyCode == 13){
			playlist_search = document.getElementById('icon_prefix');
			playlist_url = playlist_search.value;
			$.ajax({
				url : window.location.origin+'/playlist/confirm',
				method : 'GET',
				data : {
					'playlist_url' : playlist_url, 
				},
				datatype : 'json',
				success : function(response){
					var title = response.title;
					var author = response.author;
					var views = response.views;
					var videos_count = response.videos_count;
					var playlist_image = response.playlist_image;
					createConfirmPlaylistCard(title,author,views,videos_count,playlist_image);
				}
			})
		}
	}

	function clearPage(e){
		existing_card = document.getElementById('playlist_card')
		if (existing_card !== null){
			existing_card.parentNode.removeChild(existing_card);
		}
		playlist_search = document.getElementById('icon_prefix');
		playlist_search.value = '';
	}

	function loadingToast(e){
		if (e.keyCode == 13) {

		}
	}

	function init(){
		submit_button = document.getElementById('btn')
		submit_button.addEventListener('click', confirmPlaylist)
		enter_input = document.getElementById('icon_prefix')
		enter_input.addEventListener('keypress', confirmPlaylist2)
		pl_false = document.getElementById('pl-false')
		if (pl_false !== null){
			pl_false.addEventListener('click', clearPage)
		}
	}
	return {
		init: init
	};
})();