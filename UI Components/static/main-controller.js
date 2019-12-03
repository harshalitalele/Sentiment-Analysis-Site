var app = angular.module('search');

app.controller('mainCtrl', ['$scope', '$http', function($scope, $http) {
    $scope.message = "Hello there!";
    
    var obj = {
        poi_name: $scope.poi_name,
        from_date: $scope.tweet_date_f,
        to_date: $scope.tweet_date_t,
        on_this_date: $scope.tweet_date_o,
        hashtags: $scope.hashtags,
        mentions: $scope.user_mentions,
        url: $scope.tweet_urls,
        lang_e: $scope.lang_e,
        lang_p: $scope.lang_p,
        lang_h: $scope.lang_h
    };
	
	$scope.searchQuery = function() {
		$http.get('/query?q='+$scope.queryterm).then(function(res) {
			$scope.tweets = res.data;
		}, function(err) {
			$scope.message = "this is error";
		});
	};
	
	$scope.analyzeTweets = function() {
		var ids = [];
		for(var t in $scope.tweets) {
			ids.push($scope.tweets[t].id);
		}
		$http.post('/tweetanalysis', {
			query: $scope.queryterm
		}).then(function(res) {
			google.charts.load('current', {'packages':['corechart']});
			google.charts.setOnLoadCallback(drawChart);
			function drawChart() {
				var data = google.visualization.arrayToDataTable([
					['Sentiment', 'Percentage'],
					['Positive', res.data.pos],
					['Negative', res.data.neg],
					['Neutral', res.data.neut]
				]);
				var options = {'title':'Sentiment Analysis on Search Query topic over Tweets', 'width':550, 'height':400};
				var chart = new google.visualization.PieChart(document.getElementById('tweet-analysis'));
				chart.draw(data, options);
			}
		}, function(err) {
			$scope.message = "this is error";
		});
		
		$http.post('/repliesanalysis', {
			query: $scope.queryterm
		}).then(function(res) {
			google.charts.load('current', {'packages':['corechart']});
			google.charts.setOnLoadCallback(drawChart);
			function drawChart() {
				var data = google.visualization.arrayToDataTable([
					['Sentiment', 'Percentage'],
					['Positive', res.data.pos],
					['Negative', res.data.neg],
					['Neutral', res.data.neut]
				]);
				var options = {'title':'Sentiment Analysis on overall replies to the topic', 'width':550, 'height':400};
				var chart = new google.visualization.PieChart(document.getElementById('replies-analysis'));
				chart.draw(data, options);
			}
		}, function(err) {
			$scope.message = "this is error";
		});
	};
	
}]);
