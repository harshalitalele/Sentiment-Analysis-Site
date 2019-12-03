var app = angular.module('search');

app.controller('mainCtrl', ['$scope', '$http', function($scope, $http) {
    $scope.message = "Hello there!";
	var tweetReport = {},
		repliesReport = {};
    
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
		$http.get('http://192.168.1.55:5000/query?q='+$scope.queryterm).then(function(res) {
			$scope.tweets = res.data;
		}, function(err) {
			$scope.message = "this is error";
		});
	};
	
	$scope.analyzeTweets = function() {
		$scope.openModal();
		$http.post('http://192.168.1.55:5000/tweetanalysis', {
			query: $scope.queryterm
		}).then(function(res) {
			tweetReport = res.data;			
		}, function(err) {
			$scope.message = "this is error";
		});
		
		$http.post('http://192.168.1.55:5000/repliesanalysis', {
			query: $scope.queryterm
		}).then(function(res) {
			repliesReport = res.data;
		}, function(err) {
			$scope.message = "this is error";
		});
	};
	
	$scope.openModal = function() {
		$('#exampleModalLong').modal('show');
	};
	
	$('#exampleModalLong').on('shown.bs.modal', function () {
			google.charts.load('current', {'packages':['corechart']});
			google.charts.setOnLoadCallback(drawTweetChart);
			function drawTweetChart() {
				var data = google.visualization.arrayToDataTable([
					['Sentiment', 'Percentage'],
					['Positive', tweetReport.pos],
					['Negative', tweetReport.neg],
					['Neutral', tweetReport.neut]
				]);
				var options = {'title':'Sentiment Analysis on Search Query topic over Tweets', 'width':400, 'height':400};
				var chart = new google.visualization.PieChart(document.getElementById('tweet-analysis'));
				chart.draw(data, options);
			}
			google.charts.setOnLoadCallback(drawRepliesChart);
			function drawRepliesChart() {
				var data = google.visualization.arrayToDataTable([
					['Sentiment', 'Percentage'],
					['Positive', repliesReport.pos],
					['Negative', repliesReport.neg],
					['Neutral', repliesReport.neut]
				]);
				var options = {'title':'Sentiment Analysis on overall replies to the topic', 'width':400, 'height':400};
				var chart = new google.visualization.PieChart(document.getElementById('replies-analysis'));
				chart.draw(data, options);
			}
		});
	
}]);
