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
		$http.get('/query?q='+$scope.queryterm).then(function(res) {
			$scope.tweets = res.data;
		}, function(err) {
			$scope.message = "this is error";
		});
	};
	
	$scope.analyzeTweets = function() {
		$scope.openModal();
		$http.post('/queryanalysis', {
			query: $scope.queryterm
		}).then(function(res) {
			queryAnalysisReport = res.data;			
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
					['Positive', queryAnalysisReport.tweet.pos],
					['Negative', queryAnalysisReport.tweet.neg],
					['Neutral', queryAnalysisReport.tweet.neut]
				]);
				var options = {'title':'Sentiment Analysis on Search Query topic over Tweets', 'width':400, 'height':400};
				var chart = new google.visualization.PieChart(document.getElementById('tweet-analysis'));
				chart.draw(data, options);
			}
			google.charts.setOnLoadCallback(drawRepliesChart);
			function drawRepliesChart() {
				var data = google.visualization.arrayToDataTable([
					['Sentiment', 'Percentage'],
					['Positive', queryAnalysisReport.replies.pos],
					['Negative', queryAnalysisReport.replies.neg],
					['Neutral', queryAnalysisReport.replies.neut]
				]);
				var options = {'title':'Sentiment Analysis on overall replies to the topic', 'width':400, 'height':400};
				var chart = new google.visualization.PieChart(document.getElementById('replies-analysis'));
				chart.draw(data, options);
			}
		});
	
}]);
