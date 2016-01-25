var $ = require('jquery');
var React = require('react');
var ReactDOM = require('react-dom');

$(document).ready(function() {
    var EvolutionGrid = React.createClass({
        render: function() {
            var cells = [];
            this.props.evolution.map((row, step) => {
                return row.map((cellValue, x) => {
                    var key = x + ':' + step;
                    cells.push(
                        <Cell x={x} step={step} value={cellValue} key={key}/>
                    );
                });
            });
            return (
                <div>{cells}</div>
            );
        }
    });

    var Cell = React.createClass({
        render: function() {
            var leftCell = this.props.x === 0;
            var colorClass = this.props.value === 1 ? 'blackCell' : 'whiteCell';
            var classes = 'cell ' + colorClass;
            if (leftCell) classes += ' leftCell';
            //var key = this.props.x + ':' + this.props.step;
            return (
                <div className={classes}></div>
            );
        }
    });

    $.ajax({
        url: '/rule/146/JSON/',
        success: function(data) {
            var rows = data.Evolution;
            ReactDOM.render(<EvolutionGrid evolution={rows}/>, $('#array')[0]);
        }
    });

});

