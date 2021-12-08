import { Component, OnInit, Input } from '@angular/core';
import * as Highcharts from 'highcharts'
import HC_exporting from 'highcharts/modules/exporting';
import { HttpClient } from '@angular/common/http';


@Component({
  selector: 'app-widget-area',
  templateUrl: './area.component.html',
  styleUrls: ['./area.component.scss']
})
export class AreaComponent implements OnInit {

  public chartOptions: any = {};

  HighCharts = Highcharts;

  // @Input() data = [];
  public data = new Array();
  
  constructor(private http: HttpClient) { }

  ngOnInit(): void {
 
    this.http.get<any>('http://localhost:8051/continents')
      .subscribe(
        data => {
                  this.data = data;
                  // console.log(this.data);
                              
                  this.chartOptions = {
                    chart: {
                        type: 'area'
                    },
                    title: {
                        text: 'Random DATA'
                    },
                    subtitle: {
                        text: 'Demo'
                    },
                    tooltip: {
                        split: true,
                        valueSuffix: ' millions'
                    },
                    credits: {
                      enabled: false
                    },
                    exporting: {
                      enabled: true
                    },
                    series: this.data
                  };              
    });

    HC_exporting(Highcharts);

    setTimeout(() => {
      window.dispatchEvent(
        new Event('Resize')
      );
    }, 300);
  }
}