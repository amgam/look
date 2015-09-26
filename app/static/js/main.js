var app = angular.module('imgSearch', ['ngFileUpload']);

app.config(['$interpolateProvider', function($interpolateProvider) {
  $interpolateProvider.startSymbol('//');
  $interpolateProvider.endSymbol('//');
}]);

// hide initial
$("#searching").hide();
$("#query").hide();
$("#results").hide();
$("#error").hide();

app.controller('SearchCtrl', ['$scope', 'Upload', function SearchController($scope, Upload){
  $scope.data = {};
	$scope.name = "aria";
	console.log($scope.name);
	$scope.linker = "static/imgDB/"

  $scope.urlMapper = function(dict){
    var prefix = window.location.href + $scope.linker;
    var uploadPrefix = "static/upload/";
    $scope.queryImg = uploadPrefix + $scope.file.name;

    return dict.map(function(obj){
      var rObj = {};
      rObj["url"] = prefix + obj.image;
      rObj["score"] = obj.score;
      rObj["name"] = obj.image.split(".")[0];
      return rObj;
    });
  };

  $scope.submit = function() {
      $scope.upload($scope.file);
      $scope.uploadtext($scope.textfile);
  };

  // upload on file select or drop
    $scope.upload = function (file) {
      $("#searching").show();
<<<<<<< HEAD
<<<<<<< HEAD
      angular.forEach(files, function(file) {
        file.upload = Upload.upload({
          url: 'static/upload/',
          file: file
=======
=======
>>>>>>> parent of 84a0362... add multiple files

        Upload.upload({
            url: '/search',
            fields: {'username': $scope.username},
            file: file
<<<<<<< HEAD
>>>>>>> parent of 84a0362... add multiple files
=======
>>>>>>> parent of 84a0362... add multiple files
        }).progress(function (evt) {
            var progressPercentage = parseInt(100.0 * evt.loaded / evt.total);
            console.log('progress: ' + progressPercentage + '% ' + evt.config.file.name);
        }).success(function (data, status, headers, config) {
            $("#searching").hide();

            console.log('file ' + config.file.name + 'uploaded. Response: ' + data);
            // console.log(JSON.stringify(data));
            $scope.searchResults = $scope.urlMapper(data["results"]);
            console.log($scope.searchResults);
            $("#query").show();
            $("#results").show();
        }).error(function (data, status, headers, config) {
            console.log('error status: ' + status);
        });
    };

    $scope.uploadtext = function (textfile) {
      Upload.upload({
        url: 'static/querytags/',
        fields: {'textfileName': "textfile"},
        file: textfile
      }).success(function(data, status, headers, config) {
        console.log('textfile uploaded successfully')
      }).error(function(data, status, headers, config) {
        console.log('textfile upload error status: ' + status);
      }); 
    };

}]);
