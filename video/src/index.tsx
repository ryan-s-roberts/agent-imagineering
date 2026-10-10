import React from 'react';
import {Composition, registerRoot} from 'remotion';
import {Film} from './Film';
registerRoot(() => <Composition id="OntologicalSkeleton" component={Film} durationInFrames={2640} fps={30} width={1920} height={1080}/>);
