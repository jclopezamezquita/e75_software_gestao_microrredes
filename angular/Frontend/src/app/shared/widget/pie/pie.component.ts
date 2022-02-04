import { Component, OnInit, Input, SimpleChanges } from '@angular/core';
import * as Highcharts from 'highcharts'
import HC_exporting from 'highcharts/modules/exporting';
import { Measurements_24hours } from 'src/app/shared/model/measurements_24hours.model';
import { HttpClient } from '@angular/common/http';


@Component({
  selector: 'app-widget-pie',
  templateUrl: './pie.component.html',
  styleUrls: ['./pie.component.scss']
})
export class PieComponent implements OnInit {

  private intervalUpdate: any = null;

  public measurements_pcc = new Array();
  public measurements_pv = new Array();
  public measurements_genset = new Array();
  public measurements_bess = new Array();
  
  Highcharts: typeof Highcharts = Highcharts;
  updateFlag = false;
  updateData = false;

  @Input() label: string;

  chartOptions: Highcharts.Options = {
    chart: {
      plotBackgroundColor: null,
	  plotBorderWidth: null,
	  plotShadow: false,
	  type: 'pie'
    },
    title:  {
      text: 'column'
    },
    credits: {
      enabled: false
    },
    yAxis: {
      title: {
        text: 'Values [kW]'
      }
    },
    xAxis: {
      type: 'datetime'
    },
    tooltip: {
      pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
    },
    accessibility: {
      point: {
        valueSuffix: '%'
      }
    },
    exporting: {
      enabled: true
    },
    plotOptions: {
      pie: {
        allowPointSelect: true,
        cursor: 'pointer',
        dataLabels: {
          enabled: true,
            format: '<b>{point.name}</b>: {point.percentage:.1f} %'
        }
      }
    }
  }
  
  constructor(private http: HttpClient) {
  
    this.http.get<Measurements_24hours>('http://localhost:8051/v1/api/node_measurement/last_24h/')
    .subscribe(
      data2 => {
        this.measurements_pcc = [];
        this.measurements_pcc.push(Number(data2.pcc_t23));
        
        this.measurements_pv = [];
        this.measurements_pv.push(Number(data2.pv_t23));
            
        this.measurements_genset = [];
        this.measurements_genset.push(Number(data2.genset_t23));
        
        this.measurements_bess = [];
        this.measurements_bess.push(Number(data2.bess_t23));
    
        this.chartOptions.series = [
          {
            type: 'pie',
            name: 'Sources',
            colorByPoint: true,
            data: [{
                name: 'PV',
                y: Math.abs(this.measurements_pv[0])
            }, {
                name: 'PCC',
                y: Math.max(0,this.measurements_pcc[0])
            }, {
                name: 'GENSET',
                y: Math.abs(this.measurements_genset[0])
            }, {
                name: 'BESS',
                y: Math.abs(Math.min(0,this.measurements_bess[0]))
            }]
          }
        ]

        this.updateFlag = true;
        if(this.measurements_pcc.length) {
          this.updateData = true;
        }
    });
    
  }

  ngOnInit(): void {
  
    this.chartOptions.title =  {
      text: this.label
    };

    this.intervalUpdate = setInterval(function(){
      // if(this.share.mode == MODES.PLAY) {
        this.showData();
      // }
    }.bind(this), 5000);
  
  }

    private showData(): void {
      this.http.get<Measurements_24hours>('http://localhost:8051/v1/api/node_measurement/last_24h/')
      .subscribe(
        data2 => {
          this.measurements_pcc = [];
          this.measurements_pcc.push(Number(data2.pcc_t23));
          
          this.measurements_pv = [];
          this.measurements_pv.push(Number(data2.pv_t23));
              
          this.measurements_genset = [];
          this.measurements_genset.push(Number(data2.genset_t23));
          
          this.measurements_bess = [];
          this.measurements_bess.push(Number(data2.bess_t23));
      
          this.chartOptions.series = [
            {
              type: 'pie',
              name: 'Sources',
              colorByPoint: true,
              data: [{
                  name: 'PV',
                  y: Math.abs(this.measurements_pv[0])
              }, {
                  name: 'PCC',
                  y: Math.max(0,this.measurements_pcc[0])
              }, {
                  name: 'GENSET',
                  y: Math.abs(this.measurements_genset[0])
              }, {
                  name: 'BESS',
                  y: Math.abs(Math.min(0,this.measurements_bess[0]))
              }]
            }
          ]
            
          this.updateFlag = true;
          if(this.measurements_pcc.length) {
            this.updateData = true;
          }
      });
    }
  
}
