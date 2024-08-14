/* eslint-disable */
import { TypedDocumentNode as DocumentNode } from '@graphql-typed-document-node/core';
import gql from 'graphql-tag';
import * as VueApolloComposable from '@vue/apollo-composable';
import * as VueCompositionApi from '@vue/composition-api';
export type Maybe<T> = T | null;
export type InputMaybe<T> = Maybe<T>;
export type Exact<T extends { [key: string]: unknown }> = { [K in keyof T]: T[K] };
export type MakeOptional<T, K extends keyof T> = Omit<T, K> & { [SubKey in K]?: Maybe<T[SubKey]> };
export type MakeMaybe<T, K extends keyof T> = Omit<T, K> & { [SubKey in K]: Maybe<T[SubKey]> };
export type MakeEmpty<T extends { [key: string]: unknown }, K extends keyof T> = { [_ in K]?: never };
export type Incremental<T> = T | { [P in keyof T]?: P extends ' $fragmentName' | '__typename' ? T[P] : never };
export type ReactiveFunction<TParam> = () => TParam;
/** All built-in and custom scalars, mapped to their actual values */
export type Scalars = {
  ID: { input: string; output: string; }
  String: { input: string; output: string; }
  Boolean: { input: boolean; output: boolean; }
  Int: { input: number; output: number; }
  Float: { input: number; output: number; }
  /**
   * The `Date` scalar type represents a Date
   * value as specified by
   * [iso8601](https://en.wikipedia.org/wiki/ISO_8601).
   */
  Date: { input: any; output: any; }
  /**
   * The `DateTime` scalar type represents a DateTime
   * value as specified by
   * [iso8601](https://en.wikipedia.org/wiki/ISO_8601).
   */
  DateTime: { input: any; output: any; }
  /**
   * Allows use of a JSON String for input / output from the GraphQL schema.
   *
   * Use of this type is *not recommended* as you lose the benefits of having a defined, static
   * schema (one of the key benefits of GraphQL).
   */
  JSONString: { input: any; output: any; }
  /**
   * Create scalar that ignores normal serialization/deserialization, since
   * that will be handled by the multipart request spec
   */
  Upload: { input: any; output: any; }
};

export type AuthorType = {
  __typename?: 'AuthorType';
  biography?: Maybe<Scalars['String']['output']>;
  dateOfBirth?: Maybe<Scalars['Date']['output']>;
  education?: Maybe<Scalars['String']['output']>;
  firstName: Scalars['String']['output'];
  genres?: Maybe<Scalars['String']['output']>;
  id: Scalars['ID']['output'];
  influences?: Maybe<Scalars['String']['output']>;
  lastName: Scalars['String']['output'];
  location?: Maybe<Scalars['String']['output']>;
  manuscriptSet: Array<ManuscriptType>;
  middleName?: Maybe<Scalars['String']['output']>;
  nationality?: Maybe<Scalars['String']['output']>;
  notableWorks?: Maybe<Scalars['String']['output']>;
  occupation?: Maybe<Scalars['String']['output']>;
  penName?: Maybe<Scalars['String']['output']>;
  placeOfBirth?: Maybe<Scalars['String']['output']>;
  portrait?: Maybe<Scalars['String']['output']>;
  pronouns?: Maybe<Scalars['String']['output']>;
  showDateOfBirth: Scalars['Boolean']['output'];
  user: UserType;
};

export type CreateAuthor = {
  __typename?: 'CreateAuthor';
  author?: Maybe<AuthorType>;
};

export type CreateManuscript = {
  __typename?: 'CreateManuscript';
  manuscript?: Maybe<ManuscriptType>;
};

export type CreateSection = {
  __typename?: 'CreateSection';
  section?: Maybe<SectionType>;
};

export type CreateUser = {
  __typename?: 'CreateUser';
  user?: Maybe<UserType>;
};

export type CreateVoiceRecording = {
  __typename?: 'CreateVoiceRecording';
  voiceRecording?: Maybe<VoiceRecordingType>;
};

export type CreateVoiceTranscription = {
  __typename?: 'CreateVoiceTranscription';
  voiceTranscription?: Maybe<VoiceTranscriptionType>;
};

export type DeleteAuthor = {
  __typename?: 'DeleteAuthor';
  ok?: Maybe<Scalars['Boolean']['output']>;
};

export type DeleteManuscript = {
  __typename?: 'DeleteManuscript';
  ok?: Maybe<Scalars['Boolean']['output']>;
};

export type DeleteSection = {
  __typename?: 'DeleteSection';
  ok?: Maybe<Scalars['Boolean']['output']>;
};

export type DeleteUser = {
  __typename?: 'DeleteUser';
  ok?: Maybe<Scalars['Boolean']['output']>;
};

export type DeleteVoiceRecording = {
  __typename?: 'DeleteVoiceRecording';
  ok?: Maybe<Scalars['Boolean']['output']>;
};

export type DeleteVoiceTranscription = {
  __typename?: 'DeleteVoiceTranscription';
  ok?: Maybe<Scalars['Boolean']['output']>;
};

export type DocumentType = {
  __typename?: 'DocumentType';
  content?: Maybe<Scalars['String']['output']>;
  contentJson?: Maybe<Scalars['JSONString']['output']>;
  createdAt: Scalars['DateTime']['output'];
  id: Scalars['ID']['output'];
  manuscript: ManuscriptType;
  metadata?: Maybe<Scalars['JSONString']['output']>;
  order: Scalars['Int']['output'];
  section: SectionType;
  title: Scalars['String']['output'];
  updatedAt: Scalars['DateTime']['output'];
};

export type ManuscriptType = {
  __typename?: 'ManuscriptType';
  author: AuthorType;
  createdAt: Scalars['DateTime']['output'];
  documentSet: Array<DocumentType>;
  genre: VoiceWriterManuscriptGenreChoices;
  id: Scalars['ID']['output'];
  sections: Array<SectionType>;
  summary?: Maybe<Scalars['String']['output']>;
  title: Scalars['String']['output'];
  type: VoiceWriterManuscriptTypeChoices;
  updatedAt: Scalars['DateTime']['output'];
  user: UserType;
};

export type Mutation = {
  __typename?: 'Mutation';
  createAuthor?: Maybe<CreateAuthor>;
  createManuscript?: Maybe<CreateManuscript>;
  createSection?: Maybe<CreateSection>;
  createUser?: Maybe<CreateUser>;
  createVoiceRecording?: Maybe<CreateVoiceRecording>;
  createVoiceTranscription?: Maybe<CreateVoiceTranscription>;
  deleteAuthor?: Maybe<DeleteAuthor>;
  deleteManuscript?: Maybe<DeleteManuscript>;
  deleteSection?: Maybe<DeleteSection>;
  deleteUser?: Maybe<DeleteUser>;
  deleteVoiceRecording?: Maybe<DeleteVoiceRecording>;
  deleteVoiceTranscription?: Maybe<DeleteVoiceTranscription>;
  updateAuthor?: Maybe<UpdateAuthor>;
  updateManuscript?: Maybe<UpdateManuscript>;
  updateSection?: Maybe<UpdateSection>;
  updateUser?: Maybe<UpdateUser>;
  updateVoiceRecording?: Maybe<UpdateVoiceRecording>;
  updateVoiceTranscription?: Maybe<UpdateVoiceTranscription>;
};


export type MutationCreateAuthorArgs = {
  biography?: InputMaybe<Scalars['String']['input']>;
  dateOfBirth?: InputMaybe<Scalars['Date']['input']>;
  firstName: Scalars['String']['input'];
  lastName: Scalars['String']['input'];
  location?: InputMaybe<Scalars['String']['input']>;
  nationality?: InputMaybe<Scalars['String']['input']>;
  penName?: InputMaybe<Scalars['String']['input']>;
  portrait?: InputMaybe<Scalars['Upload']['input']>;
  pronouns?: InputMaybe<Scalars['String']['input']>;
  userId: Scalars['ID']['input'];
};


export type MutationCreateManuscriptArgs = {
  genre?: InputMaybe<Scalars['String']['input']>;
  manuscriptId: Scalars['ID']['input'];
  summary?: InputMaybe<Scalars['String']['input']>;
  title: Scalars['String']['input'];
  type: Scalars['String']['input'];
  userId: Scalars['ID']['input'];
};


export type MutationCreateSectionArgs = {
  manuscriptId: Scalars['ID']['input'];
  order: Scalars['Int']['input'];
  title: Scalars['String']['input'];
  type: Scalars['String']['input'];
};


export type MutationCreateUserArgs = {
  email: Scalars['String']['input'];
  firstName: Scalars['String']['input'];
  isActive?: InputMaybe<Scalars['Boolean']['input']>;
  isStaff?: InputMaybe<Scalars['Boolean']['input']>;
  isSuperuser?: InputMaybe<Scalars['Boolean']['input']>;
  lastName: Scalars['String']['input'];
  middleName?: InputMaybe<Scalars['String']['input']>;
  password: Scalars['String']['input'];
};


export type MutationCreateVoiceRecordingArgs = {
  bitrate?: InputMaybe<Scalars['Int']['input']>;
  description?: InputMaybe<Scalars['String']['input']>;
  duration?: InputMaybe<Scalars['Float']['input']>;
  file: Scalars['Upload']['input'];
  fileSize?: InputMaybe<Scalars['Int']['input']>;
  format?: InputMaybe<Scalars['String']['input']>;
  keywords?: InputMaybe<Scalars['JSONString']['input']>;
  metadata?: InputMaybe<Scalars['JSONString']['input']>;
  originalFilename?: InputMaybe<Scalars['String']['input']>;
  title: Scalars['String']['input'];
  userId: Scalars['ID']['input'];
};


export type MutationCreateVoiceTranscriptionArgs = {
  file: Scalars['Upload']['input'];
  keywords?: InputMaybe<Scalars['JSONString']['input']>;
  metadata?: InputMaybe<Scalars['JSONString']['input']>;
  provider: Scalars['String']['input'];
  recordingId: Scalars['ID']['input'];
  transcription: Scalars['String']['input'];
};


export type MutationDeleteAuthorArgs = {
  id: Scalars['ID']['input'];
};


export type MutationDeleteManuscriptArgs = {
  id: Scalars['ID']['input'];
};


export type MutationDeleteSectionArgs = {
  id: Scalars['ID']['input'];
};


export type MutationDeleteUserArgs = {
  id: Scalars['ID']['input'];
};


export type MutationDeleteVoiceRecordingArgs = {
  id: Scalars['ID']['input'];
};


export type MutationDeleteVoiceTranscriptionArgs = {
  id: Scalars['ID']['input'];
};


export type MutationUpdateAuthorArgs = {
  biography?: InputMaybe<Scalars['String']['input']>;
  dateOfBirth?: InputMaybe<Scalars['Date']['input']>;
  firstName?: InputMaybe<Scalars['String']['input']>;
  id: Scalars['ID']['input'];
  lastName?: InputMaybe<Scalars['String']['input']>;
  location?: InputMaybe<Scalars['String']['input']>;
  nationality?: InputMaybe<Scalars['String']['input']>;
  penName?: InputMaybe<Scalars['String']['input']>;
  portrait?: InputMaybe<Scalars['Upload']['input']>;
  pronouns?: InputMaybe<Scalars['String']['input']>;
};


export type MutationUpdateManuscriptArgs = {
  genre?: InputMaybe<Scalars['String']['input']>;
  id: Scalars['ID']['input'];
  summary?: InputMaybe<Scalars['String']['input']>;
  title?: InputMaybe<Scalars['String']['input']>;
  type?: InputMaybe<Scalars['String']['input']>;
};


export type MutationUpdateSectionArgs = {
  id: Scalars['ID']['input'];
  order?: InputMaybe<Scalars['Int']['input']>;
  title?: InputMaybe<Scalars['String']['input']>;
  type?: InputMaybe<Scalars['String']['input']>;
};


export type MutationUpdateUserArgs = {
  email?: InputMaybe<Scalars['String']['input']>;
  firstName?: InputMaybe<Scalars['String']['input']>;
  id: Scalars['ID']['input'];
  isActive?: InputMaybe<Scalars['Boolean']['input']>;
  isStaff?: InputMaybe<Scalars['Boolean']['input']>;
  isSuperuser?: InputMaybe<Scalars['Boolean']['input']>;
  lastName?: InputMaybe<Scalars['String']['input']>;
  middleName?: InputMaybe<Scalars['String']['input']>;
  password?: InputMaybe<Scalars['String']['input']>;
};


export type MutationUpdateVoiceRecordingArgs = {
  bitrate?: InputMaybe<Scalars['Int']['input']>;
  description?: InputMaybe<Scalars['String']['input']>;
  duration?: InputMaybe<Scalars['Float']['input']>;
  file?: InputMaybe<Scalars['String']['input']>;
  fileSize?: InputMaybe<Scalars['Int']['input']>;
  format?: InputMaybe<Scalars['String']['input']>;
  id: Scalars['ID']['input'];
  keywords?: InputMaybe<Scalars['JSONString']['input']>;
  metadata?: InputMaybe<Scalars['JSONString']['input']>;
  originalFilename?: InputMaybe<Scalars['String']['input']>;
  title?: InputMaybe<Scalars['String']['input']>;
};


export type MutationUpdateVoiceTranscriptionArgs = {
  file?: InputMaybe<Scalars['String']['input']>;
  id: Scalars['ID']['input'];
  keywords?: InputMaybe<Scalars['JSONString']['input']>;
  metadata?: InputMaybe<Scalars['JSONString']['input']>;
  provider?: InputMaybe<Scalars['String']['input']>;
  transcription?: InputMaybe<Scalars['String']['input']>;
};

export type Query = {
  __typename?: 'Query';
  allAuthors?: Maybe<Array<Maybe<AuthorType>>>;
  allDocuments?: Maybe<Array<Maybe<DocumentType>>>;
  allManuscripts?: Maybe<Array<Maybe<ManuscriptType>>>;
  allSections?: Maybe<Array<Maybe<SectionType>>>;
  allUsers?: Maybe<Array<Maybe<UserType>>>;
  allVoiceRecordings?: Maybe<Array<Maybe<VoiceRecordingType>>>;
  allVoiceTranscriptions?: Maybe<Array<Maybe<VoiceTranscriptionType>>>;
  author?: Maybe<AuthorType>;
  document?: Maybe<DocumentType>;
  manuscript?: Maybe<ManuscriptType>;
  section?: Maybe<SectionType>;
  user?: Maybe<UserType>;
  voiceRecording?: Maybe<VoiceRecordingType>;
  voiceTranscription?: Maybe<VoiceTranscriptionType>;
};


export type QueryAuthorArgs = {
  id: Scalars['ID']['input'];
};


export type QueryDocumentArgs = {
  id: Scalars['ID']['input'];
};


export type QueryManuscriptArgs = {
  id: Scalars['ID']['input'];
};


export type QuerySectionArgs = {
  id: Scalars['ID']['input'];
};


export type QueryUserArgs = {
  id: Scalars['ID']['input'];
};


export type QueryVoiceRecordingArgs = {
  id: Scalars['ID']['input'];
};


export type QueryVoiceTranscriptionArgs = {
  id: Scalars['ID']['input'];
};

export type SectionType = {
  __typename?: 'SectionType';
  createdAt: Scalars['DateTime']['output'];
  documents: Array<DocumentType>;
  id: Scalars['ID']['output'];
  manuscript: ManuscriptType;
  order: Scalars['Int']['output'];
  title: Scalars['String']['output'];
  type: VoiceWriterSectionTypeChoices;
  updatedAt: Scalars['DateTime']['output'];
};

export type UpdateAuthor = {
  __typename?: 'UpdateAuthor';
  author?: Maybe<AuthorType>;
};

export type UpdateManuscript = {
  __typename?: 'UpdateManuscript';
  manuscript?: Maybe<ManuscriptType>;
};

export type UpdateSection = {
  __typename?: 'UpdateSection';
  section?: Maybe<SectionType>;
};

export type UpdateUser = {
  __typename?: 'UpdateUser';
  user?: Maybe<UserType>;
};

export type UpdateVoiceRecording = {
  __typename?: 'UpdateVoiceRecording';
  voiceRecording?: Maybe<VoiceRecordingType>;
};

export type UpdateVoiceTranscription = {
  __typename?: 'UpdateVoiceTranscription';
  voiceTranscription?: Maybe<VoiceTranscriptionType>;
};

export type UserType = {
  __typename?: 'UserType';
  authorSet: Array<AuthorType>;
  createdAt: Scalars['DateTime']['output'];
  email: Scalars['String']['output'];
  firstName: Scalars['String']['output'];
  id: Scalars['ID']['output'];
  isActive: Scalars['Boolean']['output'];
  isStaff: Scalars['Boolean']['output'];
  isSuperuser: Scalars['Boolean']['output'];
  lastLogin?: Maybe<Scalars['DateTime']['output']>;
  lastName: Scalars['String']['output'];
  manuscriptSet: Array<ManuscriptType>;
  middleName?: Maybe<Scalars['String']['output']>;
  password: Scalars['String']['output'];
  updatedAt: Scalars['DateTime']['output'];
  voicerecordingSet: Array<VoiceRecordingType>;
};

export type VoiceRecordingType = {
  __typename?: 'VoiceRecordingType';
  bitrate?: Maybe<Scalars['Int']['output']>;
  createdAt: Scalars['DateTime']['output'];
  description?: Maybe<Scalars['String']['output']>;
  duration?: Maybe<Scalars['Float']['output']>;
  file: Scalars['String']['output'];
  fileSize?: Maybe<Scalars['Int']['output']>;
  format?: Maybe<Scalars['String']['output']>;
  id: Scalars['ID']['output'];
  isProcessed: Scalars['Boolean']['output'];
  keywords?: Maybe<Scalars['JSONString']['output']>;
  metadata?: Maybe<Scalars['JSONString']['output']>;
  originalFilename?: Maybe<Scalars['String']['output']>;
  title?: Maybe<Scalars['String']['output']>;
  transcriptions: Array<VoiceTranscriptionType>;
  updatedAt: Scalars['DateTime']['output'];
  user: UserType;
};

export type VoiceTranscriptionType = {
  __typename?: 'VoiceTranscriptionType';
  createdAt: Scalars['DateTime']['output'];
  file: Scalars['String']['output'];
  id: Scalars['ID']['output'];
  keywords?: Maybe<Scalars['JSONString']['output']>;
  metadata?: Maybe<Scalars['JSONString']['output']>;
  provider: Scalars['String']['output'];
  recording: VoiceRecordingType;
  transcription?: Maybe<Scalars['String']['output']>;
  updatedAt: Scalars['DateTime']['output'];
};

/** An enumeration. */
export enum VoiceWriterManuscriptGenreChoices {
  /** Adventure */
  Adventure = 'ADVENTURE',
  /** Art */
  Art = 'ART',
  /** Biography */
  Biography = 'BIOGRAPHY',
  /** Children */
  Children = 'CHILDREN',
  /** Cooking */
  Cooking = 'COOKING',
  /** Drama */
  Drama = 'DRAMA',
  /** Education */
  Education = 'EDUCATION',
  /** Fantasy */
  Fantasy = 'FANTASY',
  /** Fiction */
  Fiction = 'FICTION',
  /** History */
  History = 'HISTORY',
  /** Horror */
  Horror = 'HORROR',
  /** Humor */
  Humor = 'HUMOR',
  /** Multi-genre */
  MultiGenre = 'MULTI_GENRE',
  /** Music */
  Music = 'MUSIC',
  /** Mystery */
  Mystery = 'MYSTERY',
  /** Non-Fiction */
  NonFiction = 'NON_FICTION',
  /** Other */
  Other = 'OTHER',
  /** Philosophy */
  Philosophy = 'PHILOSOPHY',
  /** Poetry */
  Poetry = 'POETRY',
  /** Religion */
  Religion = 'RELIGION',
  /** Romance */
  Romance = 'ROMANCE',
  /** Science */
  Science = 'SCIENCE',
  /** Science Fiction */
  ScienceFiction = 'SCIENCE_FICTION',
  /** Self-Help */
  SelfHelp = 'SELF_HELP',
  /** Thriller */
  Thriller = 'THRILLER',
  /** Travel */
  Travel = 'TRAVEL'
}

/** An enumeration. */
export enum VoiceWriterManuscriptTypeChoices {
  /** Article */
  Article = 'ARTICLE',
  /** Blog Post */
  BlogPost = 'BLOG_POST',
  /** Book */
  Book = 'BOOK',
  /** Essay */
  Essay = 'ESSAY',
  /** Guide */
  Guide = 'GUIDE',
  /** Letter */
  Letter = 'LETTER',
  /** Manual */
  Manual = 'MANUAL',
  /** Other */
  Other = 'OTHER',
  /** Play */
  Play = 'PLAY',
  /** Poem */
  Poem = 'POEM',
  /** Report */
  Report = 'REPORT',
  /** Research Paper */
  ResearchPaper = 'RESEARCH_PAPER',
  /** Review */
  Review = 'REVIEW',
  /** Script */
  Script = 'SCRIPT',
  /** Short Story */
  ShortStory = 'SHORT_STORY',
  /** Thesis */
  Thesis = 'THESIS'
}

/** An enumeration. */
export enum VoiceWriterSectionTypeChoices {
  /** About the Author */
  AboutTheAuthor = 'ABOUT_THE_AUTHOR',
  /** Abstract */
  Abstract = 'ABSTRACT',
  /** Acknowledgements */
  Acknowledgements = 'ACKNOWLEDGEMENTS',
  /** Acknowledgments */
  Acknowledgments = 'ACKNOWLEDGMENTS',
  /** Act */
  Act = 'ACT',
  /** Afterword */
  Afterword = 'AFTERWORD',
  /** Annexes */
  Annexes = 'ANNEXES',
  /** Appendix */
  Appendix = 'APPENDIX',
  /** Bibliography */
  Bibliography = 'BIBLIOGRAPHY',
  /** Cast List */
  CastList = 'CAST_LIST',
  /** Chapter */
  Chapter = 'CHAPTER',
  /** Character List */
  CharacterList = 'CHARACTER_LIST',
  /** Conclusion */
  Conclusion = 'CONCLUSION',
  /** Copyright Page */
  CopyrightPage = 'COPYRIGHT_PAGE',
  /** Cover */
  Cover = 'COVER',
  /** Dedication */
  Dedication = 'DEDICATION',
  /** Discussion */
  Discussion = 'DISCUSSION',
  /** Epilogue */
  Epilogue = 'EPILOGUE',
  /** Executive Summary */
  ExecutiveSummary = 'EXECUTIVE_SUMMARY',
  /** Foreword */
  Foreword = 'FOREWORD',
  /** Glossary */
  Glossary = 'GLOSSARY',
  /** Index */
  Index = 'INDEX',
  /** Introduction */
  Introduction = 'INTRODUCTION',
  /** Literature Review */
  LiteratureReview = 'LITERATURE_REVIEW',
  /** Methodology */
  Methodology = 'METHODOLOGY',
  /** Other */
  Other = 'OTHER',
  /** Preface */
  Preface = 'PREFACE',
  /** Prologue */
  Prologue = 'PROLOGUE',
  /** References */
  References = 'REFERENCES',
  /** Results */
  Results = 'RESULTS',
  /** Scene */
  Scene = 'SCENE',
  /** Stage Directions */
  StageDirections = 'STAGE_DIRECTIONS',
  /** Table of Contents */
  TableOfContents = 'TABLE_OF_CONTENTS',
  /** Title Page */
  TitlePage = 'TITLE_PAGE'
}

export type GetAuthorQueryVariables = Exact<{
  id: Scalars['ID']['input'];
}>;


export type GetAuthorQuery = { __typename?: 'Query', author?: { __typename?: 'AuthorType', id: string, firstName: string, lastName: string, penName?: string | null } | null };


export const GetAuthorDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"query","name":{"kind":"Name","value":"getAuthor"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"id"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"ID"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"author"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"id"},"value":{"kind":"Variable","name":{"kind":"Name","value":"id"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}},{"kind":"Field","name":{"kind":"Name","value":"firstName"}},{"kind":"Field","name":{"kind":"Name","value":"lastName"}},{"kind":"Field","name":{"kind":"Name","value":"penName"}}]}}]}}]} as unknown as DocumentNode<GetAuthorQuery, GetAuthorQueryVariables>;
/** All built-in and custom scalars, mapped to their actual values */
export type Scalars = {
  ID: { input: string; output: string; }
  String: { input: string; output: string; }
  Boolean: { input: boolean; output: boolean; }
  Int: { input: number; output: number; }
  Float: { input: number; output: number; }
  /**
   * The `Date` scalar type represents a Date
   * value as specified by
   * [iso8601](https://en.wikipedia.org/wiki/ISO_8601).
   */
  Date: { input: any; output: any; }
  /**
   * The `DateTime` scalar type represents a DateTime
   * value as specified by
   * [iso8601](https://en.wikipedia.org/wiki/ISO_8601).
   */
  DateTime: { input: any; output: any; }
  /**
   * Allows use of a JSON String for input / output from the GraphQL schema.
   *
   * Use of this type is *not recommended* as you lose the benefits of having a defined, static
   * schema (one of the key benefits of GraphQL).
   */
  JSONString: { input: any; output: any; }
  /**
   * Create scalar that ignores normal serialization/deserialization, since
   * that will be handled by the multipart request spec
   */
  Upload: { input: any; output: any; }
};

export type AuthorType = {
  __typename?: 'AuthorType';
  biography?: Maybe<Scalars['String']['output']>;
  dateOfBirth?: Maybe<Scalars['Date']['output']>;
  education?: Maybe<Scalars['String']['output']>;
  firstName: Scalars['String']['output'];
  genres?: Maybe<Scalars['String']['output']>;
  id: Scalars['ID']['output'];
  influences?: Maybe<Scalars['String']['output']>;
  lastName: Scalars['String']['output'];
  location?: Maybe<Scalars['String']['output']>;
  manuscriptSet: Array<ManuscriptType>;
  middleName?: Maybe<Scalars['String']['output']>;
  nationality?: Maybe<Scalars['String']['output']>;
  notableWorks?: Maybe<Scalars['String']['output']>;
  occupation?: Maybe<Scalars['String']['output']>;
  penName?: Maybe<Scalars['String']['output']>;
  placeOfBirth?: Maybe<Scalars['String']['output']>;
  portrait?: Maybe<Scalars['String']['output']>;
  pronouns?: Maybe<Scalars['String']['output']>;
  showDateOfBirth: Scalars['Boolean']['output'];
  user: UserType;
};

export type CreateAuthor = {
  __typename?: 'CreateAuthor';
  author?: Maybe<AuthorType>;
};

export type CreateManuscript = {
  __typename?: 'CreateManuscript';
  manuscript?: Maybe<ManuscriptType>;
};

export type CreateSection = {
  __typename?: 'CreateSection';
  section?: Maybe<SectionType>;
};

export type CreateUser = {
  __typename?: 'CreateUser';
  user?: Maybe<UserType>;
};

export type CreateVoiceRecording = {
  __typename?: 'CreateVoiceRecording';
  voiceRecording?: Maybe<VoiceRecordingType>;
};

export type CreateVoiceTranscription = {
  __typename?: 'CreateVoiceTranscription';
  voiceTranscription?: Maybe<VoiceTranscriptionType>;
};

export type DeleteAuthor = {
  __typename?: 'DeleteAuthor';
  ok?: Maybe<Scalars['Boolean']['output']>;
};

export type DeleteManuscript = {
  __typename?: 'DeleteManuscript';
  ok?: Maybe<Scalars['Boolean']['output']>;
};

export type DeleteSection = {
  __typename?: 'DeleteSection';
  ok?: Maybe<Scalars['Boolean']['output']>;
};

export type DeleteUser = {
  __typename?: 'DeleteUser';
  ok?: Maybe<Scalars['Boolean']['output']>;
};

export type DeleteVoiceRecording = {
  __typename?: 'DeleteVoiceRecording';
  ok?: Maybe<Scalars['Boolean']['output']>;
};

export type DeleteVoiceTranscription = {
  __typename?: 'DeleteVoiceTranscription';
  ok?: Maybe<Scalars['Boolean']['output']>;
};

export type DocumentType = {
  __typename?: 'DocumentType';
  content?: Maybe<Scalars['String']['output']>;
  contentJson?: Maybe<Scalars['JSONString']['output']>;
  createdAt: Scalars['DateTime']['output'];
  id: Scalars['ID']['output'];
  manuscript: ManuscriptType;
  metadata?: Maybe<Scalars['JSONString']['output']>;
  order: Scalars['Int']['output'];
  section: SectionType;
  title: Scalars['String']['output'];
  updatedAt: Scalars['DateTime']['output'];
};

export type ManuscriptType = {
  __typename?: 'ManuscriptType';
  author: AuthorType;
  createdAt: Scalars['DateTime']['output'];
  documentSet: Array<DocumentType>;
  genre: VoiceWriterManuscriptGenreChoices;
  id: Scalars['ID']['output'];
  sections: Array<SectionType>;
  summary?: Maybe<Scalars['String']['output']>;
  title: Scalars['String']['output'];
  type: VoiceWriterManuscriptTypeChoices;
  updatedAt: Scalars['DateTime']['output'];
  user: UserType;
};

export type Mutation = {
  __typename?: 'Mutation';
  createAuthor?: Maybe<CreateAuthor>;
  createManuscript?: Maybe<CreateManuscript>;
  createSection?: Maybe<CreateSection>;
  createUser?: Maybe<CreateUser>;
  createVoiceRecording?: Maybe<CreateVoiceRecording>;
  createVoiceTranscription?: Maybe<CreateVoiceTranscription>;
  deleteAuthor?: Maybe<DeleteAuthor>;
  deleteManuscript?: Maybe<DeleteManuscript>;
  deleteSection?: Maybe<DeleteSection>;
  deleteUser?: Maybe<DeleteUser>;
  deleteVoiceRecording?: Maybe<DeleteVoiceRecording>;
  deleteVoiceTranscription?: Maybe<DeleteVoiceTranscription>;
  updateAuthor?: Maybe<UpdateAuthor>;
  updateManuscript?: Maybe<UpdateManuscript>;
  updateSection?: Maybe<UpdateSection>;
  updateUser?: Maybe<UpdateUser>;
  updateVoiceRecording?: Maybe<UpdateVoiceRecording>;
  updateVoiceTranscription?: Maybe<UpdateVoiceTranscription>;
};


export type MutationCreateAuthorArgs = {
  biography?: InputMaybe<Scalars['String']['input']>;
  dateOfBirth?: InputMaybe<Scalars['Date']['input']>;
  firstName: Scalars['String']['input'];
  lastName: Scalars['String']['input'];
  location?: InputMaybe<Scalars['String']['input']>;
  nationality?: InputMaybe<Scalars['String']['input']>;
  penName?: InputMaybe<Scalars['String']['input']>;
  portrait?: InputMaybe<Scalars['Upload']['input']>;
  pronouns?: InputMaybe<Scalars['String']['input']>;
  userId: Scalars['ID']['input'];
};


export type MutationCreateManuscriptArgs = {
  genre?: InputMaybe<Scalars['String']['input']>;
  manuscriptId: Scalars['ID']['input'];
  summary?: InputMaybe<Scalars['String']['input']>;
  title: Scalars['String']['input'];
  type: Scalars['String']['input'];
  userId: Scalars['ID']['input'];
};


export type MutationCreateSectionArgs = {
  manuscriptId: Scalars['ID']['input'];
  order: Scalars['Int']['input'];
  title: Scalars['String']['input'];
  type: Scalars['String']['input'];
};


export type MutationCreateUserArgs = {
  email: Scalars['String']['input'];
  firstName: Scalars['String']['input'];
  isActive?: InputMaybe<Scalars['Boolean']['input']>;
  isStaff?: InputMaybe<Scalars['Boolean']['input']>;
  isSuperuser?: InputMaybe<Scalars['Boolean']['input']>;
  lastName: Scalars['String']['input'];
  middleName?: InputMaybe<Scalars['String']['input']>;
  password: Scalars['String']['input'];
};


export type MutationCreateVoiceRecordingArgs = {
  bitrate?: InputMaybe<Scalars['Int']['input']>;
  description?: InputMaybe<Scalars['String']['input']>;
  duration?: InputMaybe<Scalars['Float']['input']>;
  file: Scalars['Upload']['input'];
  fileSize?: InputMaybe<Scalars['Int']['input']>;
  format?: InputMaybe<Scalars['String']['input']>;
  keywords?: InputMaybe<Scalars['JSONString']['input']>;
  metadata?: InputMaybe<Scalars['JSONString']['input']>;
  originalFilename?: InputMaybe<Scalars['String']['input']>;
  title: Scalars['String']['input'];
  userId: Scalars['ID']['input'];
};


export type MutationCreateVoiceTranscriptionArgs = {
  file: Scalars['Upload']['input'];
  keywords?: InputMaybe<Scalars['JSONString']['input']>;
  metadata?: InputMaybe<Scalars['JSONString']['input']>;
  provider: Scalars['String']['input'];
  recordingId: Scalars['ID']['input'];
  transcription: Scalars['String']['input'];
};


export type MutationDeleteAuthorArgs = {
  id: Scalars['ID']['input'];
};


export type MutationDeleteManuscriptArgs = {
  id: Scalars['ID']['input'];
};


export type MutationDeleteSectionArgs = {
  id: Scalars['ID']['input'];
};


export type MutationDeleteUserArgs = {
  id: Scalars['ID']['input'];
};


export type MutationDeleteVoiceRecordingArgs = {
  id: Scalars['ID']['input'];
};


export type MutationDeleteVoiceTranscriptionArgs = {
  id: Scalars['ID']['input'];
};


export type MutationUpdateAuthorArgs = {
  biography?: InputMaybe<Scalars['String']['input']>;
  dateOfBirth?: InputMaybe<Scalars['Date']['input']>;
  firstName?: InputMaybe<Scalars['String']['input']>;
  id: Scalars['ID']['input'];
  lastName?: InputMaybe<Scalars['String']['input']>;
  location?: InputMaybe<Scalars['String']['input']>;
  nationality?: InputMaybe<Scalars['String']['input']>;
  penName?: InputMaybe<Scalars['String']['input']>;
  portrait?: InputMaybe<Scalars['Upload']['input']>;
  pronouns?: InputMaybe<Scalars['String']['input']>;
};


export type MutationUpdateManuscriptArgs = {
  genre?: InputMaybe<Scalars['String']['input']>;
  id: Scalars['ID']['input'];
  summary?: InputMaybe<Scalars['String']['input']>;
  title?: InputMaybe<Scalars['String']['input']>;
  type?: InputMaybe<Scalars['String']['input']>;
};


export type MutationUpdateSectionArgs = {
  id: Scalars['ID']['input'];
  order?: InputMaybe<Scalars['Int']['input']>;
  title?: InputMaybe<Scalars['String']['input']>;
  type?: InputMaybe<Scalars['String']['input']>;
};


export type MutationUpdateUserArgs = {
  email?: InputMaybe<Scalars['String']['input']>;
  firstName?: InputMaybe<Scalars['String']['input']>;
  id: Scalars['ID']['input'];
  isActive?: InputMaybe<Scalars['Boolean']['input']>;
  isStaff?: InputMaybe<Scalars['Boolean']['input']>;
  isSuperuser?: InputMaybe<Scalars['Boolean']['input']>;
  lastName?: InputMaybe<Scalars['String']['input']>;
  middleName?: InputMaybe<Scalars['String']['input']>;
  password?: InputMaybe<Scalars['String']['input']>;
};


export type MutationUpdateVoiceRecordingArgs = {
  bitrate?: InputMaybe<Scalars['Int']['input']>;
  description?: InputMaybe<Scalars['String']['input']>;
  duration?: InputMaybe<Scalars['Float']['input']>;
  file?: InputMaybe<Scalars['String']['input']>;
  fileSize?: InputMaybe<Scalars['Int']['input']>;
  format?: InputMaybe<Scalars['String']['input']>;
  id: Scalars['ID']['input'];
  keywords?: InputMaybe<Scalars['JSONString']['input']>;
  metadata?: InputMaybe<Scalars['JSONString']['input']>;
  originalFilename?: InputMaybe<Scalars['String']['input']>;
  title?: InputMaybe<Scalars['String']['input']>;
};


export type MutationUpdateVoiceTranscriptionArgs = {
  file?: InputMaybe<Scalars['String']['input']>;
  id: Scalars['ID']['input'];
  keywords?: InputMaybe<Scalars['JSONString']['input']>;
  metadata?: InputMaybe<Scalars['JSONString']['input']>;
  provider?: InputMaybe<Scalars['String']['input']>;
  transcription?: InputMaybe<Scalars['String']['input']>;
};

export type Query = {
  __typename?: 'Query';
  allAuthors?: Maybe<Array<Maybe<AuthorType>>>;
  allDocuments?: Maybe<Array<Maybe<DocumentType>>>;
  allManuscripts?: Maybe<Array<Maybe<ManuscriptType>>>;
  allSections?: Maybe<Array<Maybe<SectionType>>>;
  allUsers?: Maybe<Array<Maybe<UserType>>>;
  allVoiceRecordings?: Maybe<Array<Maybe<VoiceRecordingType>>>;
  allVoiceTranscriptions?: Maybe<Array<Maybe<VoiceTranscriptionType>>>;
  author?: Maybe<AuthorType>;
  document?: Maybe<DocumentType>;
  manuscript?: Maybe<ManuscriptType>;
  section?: Maybe<SectionType>;
  user?: Maybe<UserType>;
  voiceRecording?: Maybe<VoiceRecordingType>;
  voiceTranscription?: Maybe<VoiceTranscriptionType>;
};


export type QueryAuthorArgs = {
  id: Scalars['ID']['input'];
};


export type QueryDocumentArgs = {
  id: Scalars['ID']['input'];
};


export type QueryManuscriptArgs = {
  id: Scalars['ID']['input'];
};


export type QuerySectionArgs = {
  id: Scalars['ID']['input'];
};


export type QueryUserArgs = {
  id: Scalars['ID']['input'];
};


export type QueryVoiceRecordingArgs = {
  id: Scalars['ID']['input'];
};


export type QueryVoiceTranscriptionArgs = {
  id: Scalars['ID']['input'];
};

export type SectionType = {
  __typename?: 'SectionType';
  createdAt: Scalars['DateTime']['output'];
  documents: Array<DocumentType>;
  id: Scalars['ID']['output'];
  manuscript: ManuscriptType;
  order: Scalars['Int']['output'];
  title: Scalars['String']['output'];
  type: VoiceWriterSectionTypeChoices;
  updatedAt: Scalars['DateTime']['output'];
};

export type UpdateAuthor = {
  __typename?: 'UpdateAuthor';
  author?: Maybe<AuthorType>;
};

export type UpdateManuscript = {
  __typename?: 'UpdateManuscript';
  manuscript?: Maybe<ManuscriptType>;
};

export type UpdateSection = {
  __typename?: 'UpdateSection';
  section?: Maybe<SectionType>;
};

export type UpdateUser = {
  __typename?: 'UpdateUser';
  user?: Maybe<UserType>;
};

export type UpdateVoiceRecording = {
  __typename?: 'UpdateVoiceRecording';
  voiceRecording?: Maybe<VoiceRecordingType>;
};

export type UpdateVoiceTranscription = {
  __typename?: 'UpdateVoiceTranscription';
  voiceTranscription?: Maybe<VoiceTranscriptionType>;
};

export type UserType = {
  __typename?: 'UserType';
  authorSet: Array<AuthorType>;
  createdAt: Scalars['DateTime']['output'];
  email: Scalars['String']['output'];
  firstName: Scalars['String']['output'];
  id: Scalars['ID']['output'];
  isActive: Scalars['Boolean']['output'];
  isStaff: Scalars['Boolean']['output'];
  isSuperuser: Scalars['Boolean']['output'];
  lastLogin?: Maybe<Scalars['DateTime']['output']>;
  lastName: Scalars['String']['output'];
  manuscriptSet: Array<ManuscriptType>;
  middleName?: Maybe<Scalars['String']['output']>;
  password: Scalars['String']['output'];
  updatedAt: Scalars['DateTime']['output'];
  voicerecordingSet: Array<VoiceRecordingType>;
};

export type VoiceRecordingType = {
  __typename?: 'VoiceRecordingType';
  bitrate?: Maybe<Scalars['Int']['output']>;
  createdAt: Scalars['DateTime']['output'];
  description?: Maybe<Scalars['String']['output']>;
  duration?: Maybe<Scalars['Float']['output']>;
  file: Scalars['String']['output'];
  fileSize?: Maybe<Scalars['Int']['output']>;
  format?: Maybe<Scalars['String']['output']>;
  id: Scalars['ID']['output'];
  isProcessed: Scalars['Boolean']['output'];
  keywords?: Maybe<Scalars['JSONString']['output']>;
  metadata?: Maybe<Scalars['JSONString']['output']>;
  originalFilename?: Maybe<Scalars['String']['output']>;
  title?: Maybe<Scalars['String']['output']>;
  transcriptions: Array<VoiceTranscriptionType>;
  updatedAt: Scalars['DateTime']['output'];
  user: UserType;
};

export type VoiceTranscriptionType = {
  __typename?: 'VoiceTranscriptionType';
  createdAt: Scalars['DateTime']['output'];
  file: Scalars['String']['output'];
  id: Scalars['ID']['output'];
  keywords?: Maybe<Scalars['JSONString']['output']>;
  metadata?: Maybe<Scalars['JSONString']['output']>;
  provider: Scalars['String']['output'];
  recording: VoiceRecordingType;
  transcription?: Maybe<Scalars['String']['output']>;
  updatedAt: Scalars['DateTime']['output'];
};

/** An enumeration. */
export enum VoiceWriterManuscriptGenreChoices {
  /** Adventure */
  Adventure = 'ADVENTURE',
  /** Art */
  Art = 'ART',
  /** Biography */
  Biography = 'BIOGRAPHY',
  /** Children */
  Children = 'CHILDREN',
  /** Cooking */
  Cooking = 'COOKING',
  /** Drama */
  Drama = 'DRAMA',
  /** Education */
  Education = 'EDUCATION',
  /** Fantasy */
  Fantasy = 'FANTASY',
  /** Fiction */
  Fiction = 'FICTION',
  /** History */
  History = 'HISTORY',
  /** Horror */
  Horror = 'HORROR',
  /** Humor */
  Humor = 'HUMOR',
  /** Multi-genre */
  MultiGenre = 'MULTI_GENRE',
  /** Music */
  Music = 'MUSIC',
  /** Mystery */
  Mystery = 'MYSTERY',
  /** Non-Fiction */
  NonFiction = 'NON_FICTION',
  /** Other */
  Other = 'OTHER',
  /** Philosophy */
  Philosophy = 'PHILOSOPHY',
  /** Poetry */
  Poetry = 'POETRY',
  /** Religion */
  Religion = 'RELIGION',
  /** Romance */
  Romance = 'ROMANCE',
  /** Science */
  Science = 'SCIENCE',
  /** Science Fiction */
  ScienceFiction = 'SCIENCE_FICTION',
  /** Self-Help */
  SelfHelp = 'SELF_HELP',
  /** Thriller */
  Thriller = 'THRILLER',
  /** Travel */
  Travel = 'TRAVEL'
}

/** An enumeration. */
export enum VoiceWriterManuscriptTypeChoices {
  /** Article */
  Article = 'ARTICLE',
  /** Blog Post */
  BlogPost = 'BLOG_POST',
  /** Book */
  Book = 'BOOK',
  /** Essay */
  Essay = 'ESSAY',
  /** Guide */
  Guide = 'GUIDE',
  /** Letter */
  Letter = 'LETTER',
  /** Manual */
  Manual = 'MANUAL',
  /** Other */
  Other = 'OTHER',
  /** Play */
  Play = 'PLAY',
  /** Poem */
  Poem = 'POEM',
  /** Report */
  Report = 'REPORT',
  /** Research Paper */
  ResearchPaper = 'RESEARCH_PAPER',
  /** Review */
  Review = 'REVIEW',
  /** Script */
  Script = 'SCRIPT',
  /** Short Story */
  ShortStory = 'SHORT_STORY',
  /** Thesis */
  Thesis = 'THESIS'
}

/** An enumeration. */
export enum VoiceWriterSectionTypeChoices {
  /** About the Author */
  AboutTheAuthor = 'ABOUT_THE_AUTHOR',
  /** Abstract */
  Abstract = 'ABSTRACT',
  /** Acknowledgements */
  Acknowledgements = 'ACKNOWLEDGEMENTS',
  /** Acknowledgments */
  Acknowledgments = 'ACKNOWLEDGMENTS',
  /** Act */
  Act = 'ACT',
  /** Afterword */
  Afterword = 'AFTERWORD',
  /** Annexes */
  Annexes = 'ANNEXES',
  /** Appendix */
  Appendix = 'APPENDIX',
  /** Bibliography */
  Bibliography = 'BIBLIOGRAPHY',
  /** Cast List */
  CastList = 'CAST_LIST',
  /** Chapter */
  Chapter = 'CHAPTER',
  /** Character List */
  CharacterList = 'CHARACTER_LIST',
  /** Conclusion */
  Conclusion = 'CONCLUSION',
  /** Copyright Page */
  CopyrightPage = 'COPYRIGHT_PAGE',
  /** Cover */
  Cover = 'COVER',
  /** Dedication */
  Dedication = 'DEDICATION',
  /** Discussion */
  Discussion = 'DISCUSSION',
  /** Epilogue */
  Epilogue = 'EPILOGUE',
  /** Executive Summary */
  ExecutiveSummary = 'EXECUTIVE_SUMMARY',
  /** Foreword */
  Foreword = 'FOREWORD',
  /** Glossary */
  Glossary = 'GLOSSARY',
  /** Index */
  Index = 'INDEX',
  /** Introduction */
  Introduction = 'INTRODUCTION',
  /** Literature Review */
  LiteratureReview = 'LITERATURE_REVIEW',
  /** Methodology */
  Methodology = 'METHODOLOGY',
  /** Other */
  Other = 'OTHER',
  /** Preface */
  Preface = 'PREFACE',
  /** Prologue */
  Prologue = 'PROLOGUE',
  /** References */
  References = 'REFERENCES',
  /** Results */
  Results = 'RESULTS',
  /** Scene */
  Scene = 'SCENE',
  /** Stage Directions */
  StageDirections = 'STAGE_DIRECTIONS',
  /** Table of Contents */
  TableOfContents = 'TABLE_OF_CONTENTS',
  /** Title Page */
  TitlePage = 'TITLE_PAGE'
}

export type GetAuthorQueryVariables = Exact<{
  id: Scalars['ID']['input'];
}>;


export type GetAuthorQuery = { __typename?: 'Query', author?: { __typename?: 'AuthorType', id: string, firstName: string, lastName: string, penName?: string | null } | null };


export const GetAuthorDocument = gql`
    query getAuthor($id: ID!) {
  author(id: $id) {
    id
    firstName
    lastName
    penName
  }
}
    `;

/**
 * __useGetAuthorQuery__
 *
 * To run a query within a Vue component, call `useGetAuthorQuery` and pass it any options that fit your needs.
 * When your component renders, `useGetAuthorQuery` returns an object from Apollo Client that contains result, loading and error properties
 * you can use to render your UI.
 *
 * @param variables that will be passed into the query
 * @param options that will be passed into the query, supported options are listed on: https://v4.apollo.vuejs.org/guide-composable/query.html#options;
 *
 * @example
 * const { result, loading, error } = useGetAuthorQuery({
 *   id: // value for 'id'
 * });
 */
export function useGetAuthorQuery(variables: GetAuthorQueryVariables | VueCompositionApi.Ref<GetAuthorQueryVariables> | ReactiveFunction<GetAuthorQueryVariables>, options: VueApolloComposable.UseQueryOptions<GetAuthorQuery, GetAuthorQueryVariables> | VueCompositionApi.Ref<VueApolloComposable.UseQueryOptions<GetAuthorQuery, GetAuthorQueryVariables>> | ReactiveFunction<VueApolloComposable.UseQueryOptions<GetAuthorQuery, GetAuthorQueryVariables>> = {}) {
  return VueApolloComposable.useQuery<GetAuthorQuery, GetAuthorQueryVariables>(GetAuthorDocument, variables, options);
}
export function useGetAuthorLazyQuery(variables?: GetAuthorQueryVariables | VueCompositionApi.Ref<GetAuthorQueryVariables> | ReactiveFunction<GetAuthorQueryVariables>, options: VueApolloComposable.UseQueryOptions<GetAuthorQuery, GetAuthorQueryVariables> | VueCompositionApi.Ref<VueApolloComposable.UseQueryOptions<GetAuthorQuery, GetAuthorQueryVariables>> | ReactiveFunction<VueApolloComposable.UseQueryOptions<GetAuthorQuery, GetAuthorQueryVariables>> = {}) {
  return VueApolloComposable.useLazyQuery<GetAuthorQuery, GetAuthorQueryVariables>(GetAuthorDocument, variables, options);
}
export type GetAuthorQueryCompositionFunctionResult = VueApolloComposable.UseQueryReturn<GetAuthorQuery, GetAuthorQueryVariables>;