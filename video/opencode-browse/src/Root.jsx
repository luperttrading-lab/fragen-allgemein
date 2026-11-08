import React from 'react';
import {Composition} from 'remotion';
import {Video, gesamtFrames} from './Video';

export const RemotionRoot = () => (
  <Composition id="Erklaervideo" component={Video} durationInFrames={gesamtFrames} fps={30} width={1920} height={1080} />
);
