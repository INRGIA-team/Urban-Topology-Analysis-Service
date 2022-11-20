import { Component, OnInit, ViewChild, AfterViewInit, ElementRef, OnDestroy, Input, ChangeDetectorRef } from '@angular/core';
import { FileService } from '../services/file.service';
import { FormControl } from '@angular/forms';
import {density, diameter, simpleSize} from 'graphology-metrics/graph';
import { Csv2Graph } from './csv2graph';
import { tap, zip } from 'rxjs';
import Sigma from "sigma";
import Graph from 'graphology';
import iwanthue from "iwanthue";
import forceAtlas2 from 'graphology-layout-forceatlas2';
import circular from "graphology-layout/circular";
import {AbstractGraph} from 'graphology-types';
import saveAs from './saveAsPNG';

@Component({
  selector: 'app-graph',
  templateUrl: './graph.component.html',
  styleUrls: ['./graph.component.css']
})
export class GraphComponent implements OnInit, AfterViewInit {
  @ViewChild('sigmaContainer') container!: ElementRef;
  @Input() name?: string;


  @Input() dotSize: number = 5;
  @Input() lineSize: number = 3;
  @Input() roads: boolean = false;

  metrics?: {density: number, diameter: number, simpleSize: number};

  graph!: AbstractGraph;
  renderer?: Sigma;
  palette: string[] = [];
  labelsThreshold = new FormControl<number>(0);

  constructor(
    private fileService: FileService,
    private cdRef: ChangeDetectorRef,
    private csv2graph: Csv2Graph
  ) {
    // this.graph = Graph.from(data as SerializedGraph);
    // this.graph = Graph.from(smallGraph as SerializedGraph);
    // this.palette = iwanthue(smallGraph.nodes.length, { seed: "eurSISCountryClusters" });
  }

  ngOnInit(): void {
  }

  ngAfterViewInit(): void {
    this.graph = new Graph();

    zip(
      this.fileService.readFile('/assets/graphs/nodes.csv').pipe(tap(nodesStr => this.csv2graph.getNodesFromCsv(this.graph, nodesStr, {color: 'black', size: this.dotSize}))),
      this.fileService.readFile('/assets/graphs/graph.csv').pipe(tap(edgesStr => this.csv2graph.getEdgesFromCsv(this.graph, edgesStr, {color: 'black', size: this.lineSize})))
    ).subscribe(res => {
      this.graph.addNode('adasd', {x: 1, y: 1})

      this.getMetrics();
      this.render();
    })
  }

  getMetrics(){
    this.metrics = {
      density: density(this.graph),
      diameter: diameter(this.graph),
      simpleSize: simpleSize(this.graph)
    }
    this.cdRef.detectChanges();
  }

  setAttributes(){
    const nodes = this.graph.nodes();

    this.palette = iwanthue(this.graph.nodes().length, { seed: "eurSISCountryClusters" });

    this.graph.nodes().forEach((node, i) => {
      const angle = (i * 2 * Math.PI) / this.graph.order;
      this.graph.setNodeAttribute(node, "x", nodes.length * Math.cos(angle));
      this.graph.setNodeAttribute(node, "y", nodes.length * Math.sin(angle));
      
      // const size = Math.sqrt(this.graph.degree(node)) / 2;
      const size = this.graph.degree(node) / nodes.length * 100;
      this.graph.setNodeAttribute(node, "size", size > 5 ? size : 5);

      this.graph.setNodeAttribute(node, "color", this.palette.pop());

      const label = this.graph.getNodeAttribute(node, 'name');
      this.graph.setNodeAttribute(node, "label", label);
    });

    this.graph.forEachEdge((edge, attrs: any) => {
      attrs.size = 3;
    })
    
  }

  render(){
    // initiate sigma
    if(!this.roads){
      circular.assign(this.graph);
      forceAtlas2.assign(this.graph, { settings: forceAtlas2.inferSettings(this.graph),  iterations: 600 });
    }
    // this.forceLayout = new ForceSupervisor(this.graph, {settings: {repulsion: 1, inertia: 0.3}});
    // this.forceLayout = new FA2Layout(graph, {settings: forceAtlas2.inferSettings(this.graph)});
    // this.forceLayout?.start();


    this.renderer = new Sigma(this.graph as any, this.container.nativeElement,  {renderEdgeLabels: true, renderLabels: true});
    
    this.labelsThreshold.valueChanges.subscribe(val => {
      this.renderer?.setSetting("labelRenderedSizeThreshold", + (val ? val : 0));
    })

    const labelsThreshold = this.renderer.getSetting("labelRenderedSizeThreshold");
    if(labelsThreshold) this.labelsThreshold.setValue( labelsThreshold );
    
  }


  onSaveAs(type: 'png' | 'svg'){
    if(!this.renderer) return;

    const layers = ["edges", "nodes", "labels"];  
    saveAs( type, this.renderer, layers);
  }
}
