# -*- coding: utf-8 -*-

from abaqus import *
from abaqusConstants import *
import os

os.chdir(r"C:\Users\PC\Desktop\inp")

for i in range(1, 301):
    dxf_filename = 'C:/Users/PC/Desktop/dxf/60mm_{}.dxf'.format(i)
    model_name = 'Model-{}'.format(i)

    mdb.Model(name=model_name)
    
    s = mdb.models[model_name].ConstrainedSketch(name='__profile__', sheetSize=200.0)
    s.rectangle(point1=(-80.0, -80.0), point2=(80.0, 80.0)) 
    p = mdb.models[model_name].Part(name='yaban', dimensionality=THREE_D, type=DISCRETE_RIGID_SURFACE)
    p.BaseShell(sketch=s)
    del mdb.models[model_name].sketches['__profile__'] 

    from dxf2abq import importdxf
    importdxf(fileName=dxf_filename)

    s1 = mdb.models[model_name].ConstrainedSketch(name='__profile__', sheetSize=200.0)
    s1.retrieveSketch(sketch=mdb.models['Model-1'].sketches['60mm_{}'.format(i)])
    p = mdb.models[model_name].Part(name='metamaterial', dimensionality=THREE_D, type=DEFORMABLE_BODY)
    p.BaseShellExtrude(sketch=s1, depth=25.0)
    del mdb.models[model_name].sketches['__profile__']

    p = mdb.models[model_name].parts['metamaterial']
    mdb.models[model_name].Material(name='PA12')
    mdb.models[model_name].materials['PA12'].Density(table=((1.01e-09, ),  ))
    mdb.models[model_name].materials['PA12'].Elastic(table=((427.3842, 0.3),  ))
    mdb.models[model_name].materials['PA12'].Plastic(scaleStress=None, table=(
        (40.4658, 0.0), (40.8962, 0.0022), (41.3118, 0.0045), (41.654, 0.0067), (
        41.9848, 0.0089), (42.2721, 0.0111), (42.5492, 0.0134), (42.7862, 0.0157), 
        (43.0035, 0.0178), (43.2051, 0.0201), (43.3939, 0.0223), (43.5645, 0.0246), 
        (43.7179, 0.0268), (43.8621, 0.029), (44.0121, 0.0313), (44.1231, 0.0335), 
        (44.2307, 0.0358), (44.3279, 0.038), (44.4242, 0.0402), (44.4643, 0.0425)))

    mdb.models[model_name].HomogeneousShellSection(name='s12-1', preIntegrate=OFF, 
        material='PA12', thicknessType=UNIFORM, thickness=1.2, thicknessField='', 
        nodalThicknessField='', idealization=NO_IDEALIZATION, 
        poissonDefinition=DEFAULT, thicknessModulus=None, temperature=GRADIENT, 
        useDensity=OFF, integrationRule=SIMPSON, numIntPts=5)

    p = mdb.models[model_name].parts['metamaterial']
    faces = p.faces
    region = (faces,) 
    p.SectionAssignment(region=region, sectionName='s12-1')

    a = mdb.models[model_name].rootAssembly
    a.DatumCsysByDefault(CARTESIAN)
    p = mdb.models[model_name].parts['metamaterial']
    a.Instance(name='metamaterial-1', part=p, dependent=ON)
    p = mdb.models[model_name].parts['yaban']
    a.Instance(name='yaban-1', part=p, dependent=ON)
    p = a.instances['yaban-1']
    p.translate(vector=(156.0, 0.0, 0.0))
    a = mdb.models[model_name].rootAssembly
    p = mdb.models[model_name].parts['yaban']
    a.Instance(name='yaban-2', part=p, dependent=ON)
    p = a.instances['yaban-2']
    p.translate(vector=(332.0, 0.0, 0.0))
    a = mdb.models[model_name].rootAssembly
    a.rotate(instanceList=('yaban-1', 'yaban-2'), axisPoint=(76.0, 0.0, 0.0), 
        axisDirection=(160.0, 0.0, 0.0), angle=90.0)
    p = mdb.models[model_name].parts['yaban']
    e = p.edges
    p.DatumPointByMidPoint(point1=p.InterestingPoint(edge=e[3], rule=MIDDLE), 
        point2=p.InterestingPoint(edge=e[1], rule=MIDDLE))
    p = mdb.models[model_name].parts['yaban']
    v, e1, d, n = p.vertices, p.edges, p.datums, p.nodes
    p.ReferencePoint(point=d[2])
    p = mdb.models[model_name].parts['yaban']
    r = p.referencePoints
    refPoints=(r[3], )
    p.Set(referencePoints=refPoints, name='yb')
    a = mdb.models[model_name].rootAssembly
    a.regenerate()
    a = mdb.models[model_name].rootAssembly
    a.translate(instanceList=('yaban-1', ), vector=(-126.0, 60.0, 12.5))
    a.translate(instanceList=('yaban-2', ), vector=(-302.0, 0.0, 12.5))


    mdb.models[model_name].ExplicitDynamicsStep(name='Step-1', previous='Initial', 
        improvedDtMethod=ON) 
    regionDef=mdb.models[model_name].rootAssembly.sets['yaban-1.yb']   
    mdb.models[model_name].HistoryOutputRequest(name='H-Output-1', 
        createStepName='Step-1', variables=('U2', 'RF2'), region=regionDef, 
        sectionPoints=DEFAULT, rebar=EXCLUDE)
    mdb.models[model_name].ContactProperty('IntProp-1')
    mdb.models[model_name].interactionProperties['IntProp-1'].TangentialBehavior(
        formulation=PENALTY, directionality=ISOTROPIC, slipRateDependency=OFF, 
        pressureDependency=OFF, temperatureDependency=OFF, dependencies=0, table=((
        0.25, ), ), shearStressLimit=None, maximumElasticSlip=FRACTION, 
        fraction=0.005, elasticSlipStiffness=None)
    mdb.models[model_name].interactionProperties['IntProp-1'].NormalBehavior(
        pressureOverclosure=HARD, allowSeparation=ON, 
        constraintEnforcementMethod=DEFAULT)

    mdb.models[model_name].ContactExp(name='Int-1', createStepName='Initial')
    mdb.models[model_name].interactions['Int-1'].includedPairs.setValuesInStep(
        stepName='Initial', useAllstar=ON)
    mdb.models[model_name].interactions['Int-1'].contactPropertyAssignments.appendInStep(
        stepName='Initial', assignments=((GLOBAL, SELF, 'IntProp-1'), ))
    
    a = mdb.models[model_name].rootAssembly
    r1 = a.instances['yaban-2'].referencePoints
    refPoints1=(r1[3], )
    region = a.Set(referencePoints=refPoints1, name='Set-3')
    mdb.models[model_name].EncastreBC(name='BC-1', createStepName='Step-1', 
        region=region, localCsys=None)
    mdb.models[model_name].TabularAmplitude(name='Amp-1', timeSpan=STEP, 
        smooth=SOLVER_DEFAULT, data=((0.0, 0.0), (1.0, 1.0)))
    a = mdb.models[model_name].rootAssembly
    r1 = a.instances['yaban-1'].referencePoints
    refPoints1=(r1[3], )
    region = a.Set(referencePoints=refPoints1, name='Set-4')
    mdb.models[model_name].DisplacementBC(name='BC-2', createStepName='Step-1', 
        region=region, u1=0.0, u2=-55.0, u3=0.0, ur1=0.0, ur2=0.0, ur3=0.0, 
        amplitude='Amp-1', fixed=OFF, distributionType=UNIFORM, fieldName='', 
        localCsys=None)
    p = mdb.models[model_name].parts['metamaterial']
    p.setMeshControls(regions=p.faces, elemShape=QUAD, technique=STRUCTURED)
    p.seedPart(size=0.8, deviationFactor=0.1, minSizeFactor=0.1)
    p.generateMesh()
    p = mdb.models[model_name].parts['yaban']
    p.setMeshControls(regions=p.faces, elemShape=QUAD, technique=STRUCTURED)
    p.seedPart(size=8.0, deviationFactor=0.1, minSizeFactor=0.1)
    p.generateMesh()

    job_name = "Job-{}".format(i)
    mdb.Job(name=job_name, model=model_name, type=ANALYSIS, 
            atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=90, 
            memoryUnits=PERCENTAGE, explicitPrecision=SINGLE, 
            nodalOutputPrecision=SINGLE, echoPrint=OFF, modelPrint=OFF, 
            contactPrint=OFF, historyPrint=OFF, userSubroutine='', scratch='', 
            resultsFormat=ODB, parallelizationMethodExplicit=DOMAIN, 
            numDomains=6, activateLoadBalancing=False, numThreadsPerMpiProcess=1, 
            multiprocessingMode=DEFAULT, numCpus=6)

    mdb.jobs[job_name].writeInput(consistencyChecking=OFF)
    print("Generated .inp file for {}".format(job_name))
