import { Component, OnInit, Input, SimpleChanges } from '@angular/core';
import * as Highcharts from 'highcharts'
import HC_exporting from 'highcharts/modules/exporting';


@Component({
  selector: 'app-widget-area',
  templateUrl: './area.component.html',
  styleUrls: ['./area.component.scss']
})
export class AreaComponent {

  Highcharts: typeof Highcharts = Highcharts;
  updateFlag = false;
  updateData = false;

  @Input() label: string;
  @Input() data_pcc = [];
  @Input() data_pv = [];
  @Input() data_genset = [];
  @Input() data_bess = [];

  chartOptions: Highcharts.Options = {
    title:  {
      text: 'column'
    }, 
    series: [
      {
        type: 'area',
        name: 'PCC',
        data: this.data_pcc
      },{
        type: 'area',
        name: 'PV',
        data: this.data_pv
      },{
        type: 'area',
        name: 'BESS',
        data: this.data_bess
      },{
        type: 'area',
        name: 'GENSET',
        data: this.data_genset
      }
    ]
  }
  
  constructor() {  }

  ngOnInit(): void { }

  ngOnChanges(changes: SimpleChanges) {
  
    this.chartOptions.title =  {
      text: this.label
    };

    // this.chartOptions.series[0] = {
    //   type: 'area',
    //   data: [this.data_pcc, this.data_pv]
    // }

    this.chartOptions.series = [
      {
        type: 'area',
        name: 'PCC',
        data: this.data_pcc
      },{
        type: 'area',
        name: 'PV',
        data: this.data_pv
      },{
        type: 'area',
        name: 'BESS',
        data: this.data_bess
      },{
        type: 'area',
        name: 'GENSET',
        data: this.data_genset
      }
    ]

    this.updateFlag = true;
    if(this.data_pcc.length) {
      this.updateData = true;
    }
    console.log("********* ngOnChanges ********")
    console.log(this.chartOptions.series[0])

  }
}