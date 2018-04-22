import React, { Component } from 'react';

class Menu extends Component {
  render() {
    return (
      <div className="ui fixed inverted menu">
        <div className="ui container">
          <a href="/" className="header item">
            <img className="logo" alt="logo" src={require('../img/lightware.png')} />{this.props.title}</a>
          <a href="/" className="item">Home</a>
          <div className="ui simple dropdown item">Menu<i className="dropdown icon"></i>
            <div className="menu">
              <a className="item" href="/">Log-in</a>
              <div className="divider"></div>

              <a className="item" href="/">Reset</a>
            </div>
          </div>
        </div>
      </div>);
  }
}

export default Menu;
