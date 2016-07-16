var playlistDownload = (function(){
	var playlist_url = "";
	function downloadAll(e){
		e.preventDefault();
		setTimeout(function(){Materialize.toast('This may take some time. Be patient', 35000, 'rounded')},2000);
		var input = $("input[id='mycheckbox']")
		if (input.length <= 16){
			console.log("<16")
			var index_list=[];
			for(var i=0;i<input.length;i++){
				index_list.push(i+1)
			}
			console.log(index_list)
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
					list_videos = response.list_downloads
					for(i=0;i<list_videos.length;i++){
						window.open(list_videos[i],'_blank')
						self.focus()
					}
				}
			})
		}
		else if (input.length > 16 & input.length <= 32){
			console.log(">16")
			var index_list=[];
			for(var i=0;i<input.length/2;i++){
				index_list.push(i+1)
			}
			console.log(index_list)
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
					list_videos = response.list_downloads
					for(i=0;i<list_videos.length;i++){
						window.open(list_videos[i],'_blank')
						self.focus()
					}
					var index_list=[];
					for(var i=Math.ceil(input.length/2);i<input.length;i++){
						index_list.push(i+1)
					}
					console.log(index_list)
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
							list_videos = response.list_downloads
							for(i=0;i<list_videos.length;i++){
								window.open(list_videos[i],'_blank')
								self.focus()
							}
						}
					})
				}
			})
		}
		else if(input.length>32){
			console.log(">40")
			var index_list=[];
			for(var i=0;i<input.length/4;i++){
				index_list.push(i+1)
			}
			console.log(index_list)
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
					list_videos = response.list_downloads
					for(i=0;i<list_videos.length;i++){
						window.open(list_videos[i],'_blank')
						self.focus()
					}
					var index_list=[];
					for(var i=Math.ceil(input.length/4);i<input.length/2;i++){
						index_list.push(i+1)
					}
					console.log(index_list)
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
							list_videos = response.list_downloads
							for(i=0;i<list_videos.length;i++){
								window.open(list_videos[i],'_blank')
								self.focus()
							}
							var index_list=[];
							for(var i=Math.ceil(input.length/2);i<3*(input.length/4);i++){
								index_list.push(i+1)
							}
							console.log(index_list)
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
									list_videos = response.list_downloads
									for(i=0;i<list_videos.length;i++){
										window.open(list_videos[i],'_blank')
										self.focus()
									}
									var index_list=[];
									for(var i=Math.ceil(3*(input.length/4));i<input.length;i++){
										index_list.push(i+1)
									}
									console.log(index_list)
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
											list_videos = response.list_downloads
											for(i=0;i<list_videos.length;i++){
												window.open(list_videos[i],'_blank')
												self.focus()
											}
										}
									})
								}
							})
						}
					})
				}
			})
		}
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
				list_videos = response.list_downloads
				for(i=0;i<list_videos.length;i++){
					window.open(list_videos[i])
				}
			}
		})
	}

	function init(){
		query = window.location.search
		for(i=5;i<query.length;i++){
			playlist_url = playlist_url + query[i];
		}
		Materialize.toast('Please disable POP-UP BLOCK for this website. Thanks', 20000, 'rounded')
		button_all = document.getElementById('btn-all');
		button_all.addEventListener('click',downloadAll)
		button_some = document.getElementById('btn');
		button_some.addEventListener('click',downloadSome);
	}
	return {
		init: init
	};
})();