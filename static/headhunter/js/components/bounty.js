'use strict';

var converter = new Showdown.converter();

// BountyBox
var BountyBox = React.createClass({displayName: 'BountyBox',
  loadBountiesFromServer: function() {
    $.ajax({
      url: this.props.url,
      dataType: 'json',
      success: function(data) {
        this.setState({data: data});
      }.bind(this),
      error: function(xhr, status, err) {
        console.error(this.props.url, status, err.toString());
      }.bind(this)
    });
  },
  handleBountySubmit: function(bounty) {
    $.ajax({
      url: this.props.url,
      dataType: 'json',
      type: 'POST',
      data: bounty,
      success: function(data) {
        this.setState({data: data});
      }.bind(this),
      error: function(xhr, status, err) {
        console.error(this.props.url, status, err.toString());
      }.bind(this)
    });
  },
  getInitialState: function() {
    return {data: []};
  },
  componentDidMount: function() {
    this.loadBountiesFromServer();
    setInterval(this.loadBountiesFromServer, this.props.pollInterval);
  },
  render: function() {
    return (
      React.createElement("div", {className: "BountyBox"}, 
        React.createElement("h1", null, "Bounties"), 
        React.createElement(BountyList, {data: this.state.data}), 
        React.createElement(BountyForm, {onBountySubmit: this.handleBountySubmit})
      )
    );
  }
});

var BountyList = React.createClass({displayName: 'BountyList',
  render: function() {
    var bountyNodes = this.props.data.map(function (bounty) {
      return (
        React.createElement(
          Bounty, {
            source_character: bounty.fields.source_character,
            source_realm: bounty.fields.source_realm}, 
          bounty.fields.description
        )
      );
    });
    return (
      React.createElement("div", {className: "BountyList"}, 
        bountyNodes
      )
    );
  }
});

var BountyForm = React.createClass({displayName: 'BountyForm',
  handleSubmit: function(e) {
    e.preventDefault();
    var region = React.findDOMNode(this.refs.region).value.trim();
    var sourceRealm = React.findDOMNode(this.refs.sourceRealm).value.trim();
    var sourceCharacter = React.findDOMNode(this.refs.sourceCharacter).value.trim();
    var destinationRealm = React.findDOMNode(this.refs.destinationRealm).value.trim();
    var destinationCharacter = React.findDOMNode(this.refs.destinationCharacter).value.trim();
    var description = React.findDOMNode(this.refs.description).value.trim();
    var reward = React.findDOMNode(this.refs.reward).value.trim();
    if (
        !region || !sourceRealm || !sourceCharacter ||
        !destinationRealm || !destinationCharacter ||
        !description || !reward) 
      return;

    this.props.onBountySubmit({
      region: region,
      source_realm: sourceRealm,
      source_character: sourceCharacter,
      destination_realm: destinationRealm,
      destination_character: destinationCharacter,
      description: description,
      reward: reward
    });

    React.findDOMNode(this.refs.region).value = '';
    React.findDOMNode(this.refs.sourceRealm).value = '';
    React.findDOMNode(this.refs.sourceCharacter).value = '';
    React.findDOMNode(this.refs.destinationRealm).value = '';
    React.findDOMNode(this.refs.destinationCharacter).value = '';
    React.findDOMNode(this.refs.description).value = '';
    React.findDOMNode(this.refs.reward).value = '';
  },
  render: function() {
    return (
      React.createElement('form', {className: "bountyForm", onSubmit: this.handleSubmit},
        React.createElement('input', {type: "text", placeholder: "Region", ref: "region"}),
        React.createElement('input', {type: "text", placeholder: "Source realm", ref: "sourceRealm"}),
        React.createElement('input', {type: "text", placeholder: "Source character", ref: "sourceCharacter"}),
        React.createElement('input', {type: "text", placeholder: "Destination realm", ref: "destinationRealm"}),
        React.createElement('input', {type: "text", placeholder: "Destination character", ref: "destinationCharacter"}),
        React.createElement('input', {type: "text", placeholder: "Description", ref: "description"}),
        React.createElement('input', {type: "text", placeholder: "Reward", ref: "reward"}),
        React.createElement('input', {type: "submit", value: "Save"})
      )
    )
  }
});

var Bounty = React.createClass({displayName: "Bounty",
  render: function() {
    var rawMarkup = converter.makeHtml(this.props.children.toString());
    return (
      React.createElement("div", {className: "bounty"}, 
        React.createElement("h2", {className: "bountySource"}, 
          this.props.source_character + " - " + this.props.source_realm
        ),
        React.createElement("span", {dangerouslySetInnerHTML: {__html: rawMarkup}})
      )
    );
  }
});

React.render(
  React.createElement(BountyBox, {url: "/api/bounty", pollInterval: 10000}),
  document.getElementById('bounty-box')
);
