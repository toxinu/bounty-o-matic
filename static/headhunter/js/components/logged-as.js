var LoggedAs = React.createClass({displayName: "LoggedAs",
  getInitialState: function() {
    return {loggedAs: null};
  },
  componentDidMount: function() {
    $.ajax({
      url: this.props.url,
      dataType: 'json',
      success: function(data) {
        this.setState({loggedAs: data});
        $("#logged-as").css('display', 'block');
      }.bind(this),
      error: function(xhr, status, err) {
        console.error(this.props.url, status, err.toString());
      }.bind(this)
    });
  },
  render: function() {
    return (
      React.createElement("li", {className: "loggedAs"}, 
        "BattleTag: " + this.state.loggedAs)
    );
  }
});

React.render(
  React.createElement(LoggedAs, {url: '/api/player-battletag'}),
  document.getElementById('logged-as')
);